from django.db import models


class Well(models.Model):
    region = models.CharField('Регион', max_length=25, blank=True, null=True)
    name_mst = models.CharField('Месторождение', max_length=100, blank=True, null=True)
    plosh = models.CharField('Площадь', max_length=256, blank=True, null=True)
    n_lic = models.CharField('Номер лицензии', max_length=25, blank=True, null=True)
    lic = models.CharField('Название лицензионного участка', max_length=256, blank=True, null=True)
    n_kust = models.CharField('Номер куста', max_length=25, blank=True, null=True)
    n_skv = models.CharField('Номер скважины', max_length=10, blank=True, null=True)
    tip_skv = models.CharField('Тип скважины', max_length=25, blank=True, null=True)
    sk_zb = models.FloatField('Отметка забоя, м', blank=True, null=True)
    altit = models.FloatField('Альтитуда ротора, м', blank=True, null=True)
    d_zaboi = models.FloatField('Давление забоя, МПа', blank=True, null=True)
    d_plast = models.FloatField('Давление пластовое, МПа', blank=True, null=True)
    d_skv = models.FloatField('Диаметр скважины, мм', blank=True, null=True)
    x = models.CharField('Координата X', max_length=50, blank=True, null=True)
    y = models.CharField('Координата Y', max_length=50, blank=True, null=True)
    id_strat = models.CharField('Индекс пласта', max_length=50, blank=True, null=True)
    strat = models.CharField('Название пласта', max_length=100, blank=True, null=True)
    abs_o_k = models.FloatField('Абсолютная отметка кровли, м', blank=True, null=True)
    abs_o_p = models.FloatField('Абсолютная отметка подошвы, м', blank=True, null=True)
    shtucr = models.FloatField('Штутцер, мм', blank=True, null=True)
    debit_n = models.FloatField('Дебит нефти, т/сут', blank=True, null=True)
    uvp_n = models.FloatField('Удельный вес нефти, т/м3', blank=True, null=True)
    debit_v = models.FloatField('Дебит воды, т/сут', blank=True, null=True)
    debit_g = models.FloatField('Дебит газа, куб.м/сут', blank=True, null=True)
    debit_k = models.FloatField('Дебит конденсата, т/сут', blank=True, null=True)
    char_nas = models.CharField('Характер насыщения', max_length=50, blank=True, null=True)
    m_otl = models.FloatField('Эффективная мощность отложений, м', blank=True, null=True)
    o_rab = models.DateField('Дата окончания бурения', blank=True, null=True)
    id_xy = models.CharField('ID_XY', max_length=50, blank=True, null=True)
    auth = models.CharField('Автор записи', max_length=50, blank=True, null=True)
    material_available = models.CharField('Наличие материала', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Скважина'
        verbose_name_plural = 'Скважины'

    def __str__(self):
        return f"{self.name_mst or 'скважина'} {self.n_skv or ''}" 
