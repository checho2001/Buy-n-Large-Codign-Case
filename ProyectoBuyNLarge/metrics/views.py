from collections import defaultdict

from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import defaultdict
from operator import itemgetter



from inventory.models import Product  # Importa tu modelo de Producto


class KPIView(APIView):
    ### KPIs

    @staticmethod
    def calcular_valor_inventario_total():
        # Sumatoria de (price * stock) para todos los productos
        total = Product.objects.aggregate(
            valor_total=Sum(F('price') * F('stock'))
        )['valor_total'] or 0
        return total

    @staticmethod
    def contar_productos_stock_bajo(umbral=10):
        # Productos con stock menor al umbral (default 10)
        return Product.objects.filter(stock__lt=umbral).count()

    @staticmethod
    def contar_productos_agotados():
        # Productos con stock = 0
        return Product.objects.filter(stock=0).count()

    @staticmethod
    def contar_productos_nuevos_mes_actual():
        # Productos creados este mes
        hoy = timezone.now()
        primer_dia_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return Product.objects.filter(created_at__gte=primer_dia_mes).count()
    
    def get(self, request):
        kpis = {
            'valor_inventario_total': KPIView.calcular_valor_inventario_total(),
            'productos_stock_bajo': KPIView.contar_productos_stock_bajo(umbral=10),
            'productos_agotados': KPIView.contar_productos_agotados(),
            'productos_nuevos_mes_actual': KPIView.contar_productos_nuevos_mes_actual(),
        }
        print(kpis)
        return Response(kpis)


### Graphics and charts

class GraphicsView(APIView):
    # 1. Distribución por Categoría/Brand

    def datos_distribucion_stock(grupo_por='category'):
        """
        Parámetros: 'category' o 'brand'
        Retorna: {labels: [], datos: []} para gráfico de dona/barras
        """
        grouped = Product.objects.values(grupo_por).annotate(
            total_stock=Sum('stock')
        ).order_by('-total_stock')
        
        return {
            'labels': [item[grupo_por] for item in grouped],
            'datos': [item['total_stock'] for item in grouped]
        }

    def datos_mapa_arbol():
        """
        Retorna estructura jerárquica para mapa de árbol:
        Brand -> Categorías -> Stock total
        """
        estructura = []
        brands = Product.objects.values('brand').distinct()
        
        for brand in brands:
            categorias = Product.objects.filter(brand=brand['brand']).values(
                'category'
            ).annotate(
                total_stock=Sum('stock')
            )
            estructura.append({
                'name': brand['brand'],
                'children': [
                    {'name': cat['category'], 'value': cat['total_stock']}
                    for cat in categorias
                ]
            })
        
        return estructura


    # 2. Análisis de Características Técnicas

    def datos_barras_agrupadas_features(feature_keys=['ram', 'storage']):
        """
        Parámetros: Lista de características a combinar
        Retorna: Combinaciones únicas y su stock total
        """
        combinaciones = defaultdict(int)
        
        for product in Product.objects.all():
            key = " + ".join(
                [product.features.get(k, 'N/A') for k in feature_keys]
            )
            combinaciones[key] += product.stock
        
        return {
            'labels': list(combinaciones.keys()),
            'datos': list(combinaciones.values())
        }


    # 3. Evolución Temporal

    def datos_linea_tiempo(rango_meses=12):
        """
        Parámetros: Cantidad de meses a visualizar
        Retorna: Evolución mensual del stock total
        """
        data = Product.objects.annotate(
            mes=TruncMonth('created_at')
        ).values('mes').annotate(
            total_stock=Sum('stock')
        ).order_by('mes')[:rango_meses]
        
        return {
            'fechas': [item['mes'].strftime('%Y-%m') for item in data],
            'stock': [item['total_stock'] for item in data]
        }

    def datos_areas_apiladas(rango_meses=6):
        """
        Parámetros: Cantidad de meses a visualizar
        Retorna: Evolución por categoría
        """
        categories = Product.objects.values_list('category', flat=True).distinct()
        result = {'fechas': []}
        
        for cat in categories:
            data = Product.objects.filter(category=cat).annotate(
                mes=TruncMonth('created_at')
            ).values('mes').annotate(
                total_stock=Sum('stock')
            ).order_by('mes')[:rango_meses]
            
            if not result['fechas']:
                result['fechas'] = [d['mes'].strftime('%Y-%m') for d in data]
            
            result[cat] = [d['total_stock'] for d in data]
        
        return result
    
    def get(self, request):
        datos = {
            'distribucion_stock': self.datos_distribucion_stock(),
            'mapa_arbol': self.datos_mapa_arbol(),
            'barras_agrupadas_features': self.datos_barras_agrupadas_features(),
            'linea_tiempo': self.datos_linea_tiempo(),
            'areas_apiladas': self.datos_areas_apiladas()
        }
        return Response(datos)

## tablas

class TablaView(APIView):

    def top_productos_stock_bajo(limite=5):
        """
        Retorna los productos con menor stock
        """
        productos = Product.objects.order_by('stock').values(
            'name',
            'category',
            'brand',
            'stock'
        )[:limite]
        
        return list(productos)

    def top_movimientos_recientes(limite=5):
        """
        Productos con actualizaciones más recientes
        """
        productos = Product.objects.order_by('-updated_at').values(
            'name',
            'category',
            'stock',
            'updated_at'
        )[:limite]
        
        # Formatear fecha para mejor visualización
        for p in productos:
            p['updated_at'] = p['updated_at'].strftime('%Y-%m-%d %H:%M')
        
        return list(productos)

    def top_combinaciones_caracteristicas(limite=5):
        """
        Ranking de combinaciones de features con mayor stock
        """
        combinaciones = defaultdict(int)
        
        # Procesar todos los productos
        for product in Product.objects.only('features', 'stock'):
            if product.features:
                # Crear clave única ordenada para características
                features = sorted(product.features.items())
                clave = ", ".join([f"{k}:{v}" for k, v in features])
                combinaciones[clave] += product.stock
            else:
                combinaciones['Sin características'] += product.stock
        
        # Ordenar y seleccionar top
        sorted_comb = sorted(
            combinaciones.items(),
            key=itemgetter(1),
            reverse=True
        )[:limite]
        
        return [{'combinacion': k, 'stock_total': v} for k, v in sorted_comb]
    
    def get(self, request):
        tablas = {
            'productos_stock_bajo': self.top_productos_stock_bajo(),
            'movimientos_recientes': self.top_movimientos_recientes(),
            'combinaciones_caracteristicas': self.top_combinaciones_caracteristicas()
        }
        return Response(tablas)
