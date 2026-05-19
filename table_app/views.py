from django.db.models import F, Value, CharField, IntegerField, Max, Case, When, Q
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, render

from .models import Well


def home(request):
    qs = Well.objects.all()

    region = request.GET.get('region', '').strip()
    name_mst = request.GET.get('name_mst', '').strip()
    plosh = request.GET.get('plosh', '').strip()
    n_skv = request.GET.get('n_skv', '').strip()
    id_xy = request.GET.get('id_xy', '').strip()
    has_tests = request.GET.get('has_tests', '')

    if region:
        qs = qs.filter(region__icontains=region)
    if name_mst:
        qs = qs.filter(name_mst__icontains=name_mst)
    if plosh:
        qs = qs.filter(plosh__icontains=plosh)
    if n_skv:
        qs = qs.filter(n_skv__icontains=n_skv)
    if id_xy:
        qs = qs.filter(id_xy__icontains=id_xy)

    qs = qs.annotate(
        group_key=Case(
            When(id_xy__isnull=False, id_xy__gt='', then=F('id_xy')),
            default=Concat(Value('ROW_'), F('pk'), output_field=CharField()),
            output_field=CharField(),
        )
    )

    wells = (
        qs.values('group_key')
        .annotate(
            id=Max('pk'),
            region=Max('region'),
            name_mst=Max('name_mst'),
            plosh=Max('plosh'),
            n_skv=Max('n_skv'),
            id_xy=Max('id_xy'),
            has_tests=Max(
                Case(
                    When(
                        Q(abs_o_k__isnull=False) | Q(abs_o_p__isnull=False),
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
        )
        .order_by('region', 'name_mst', 'n_skv')
    )

    if has_tests == 'yes':
        wells = wells.filter(has_tests=1)
    elif has_tests == 'no':
        wells = wells.filter(has_tests=0)

    context = {
        'wells': wells,
        'total_count': wells.count(),
        'filters': {
            'region': region,
            'name_mst': name_mst,
            'plosh': plosh,
            'n_skv': n_skv,
            'id_xy': id_xy,
            'has_tests': has_tests,
        },
    }
    return render(request, 'table_app/home.html', context)


def well_detail(request, pk):
    selected = get_object_or_404(Well, pk=pk)
    if selected.id_xy:
        records = Well.objects.filter(id_xy=selected.id_xy).order_by('pk')
    else:
        records = Well.objects.filter(pk=selected.pk)

    has_tests = records.filter(Q(abs_o_k__isnull=False) | Q(abs_o_p__isnull=False)).exists()

    return render(
        request,
        'table_app/well_detail.html',
        {
            'selected': selected,
            'records': records,
            'has_tests': has_tests,
        },
    )
