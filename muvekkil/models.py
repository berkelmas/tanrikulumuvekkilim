from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_delete
from django.dispatch import receiver

# Burada Django'nun bizim için hazırladığı User sınıfımızı genişletelim.

"""
Genişlettiğimiz User sınıfında yapacaklarımız.
1) Giriş için username değil; email adresi kullanılacak.
2) Kullanıcının doğum tarihi eklemesi yapılacak.
"""

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    email = models.EmailField(('Müvekkil Email'), unique=True)
    birth_date= models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = ('Müvekkil')
        verbose_name_plural = _('Müvekkiller')

    def __str__(self):
        return self.get_full_name();

"""
Burada kullanıcı modelimizi oluşturduk ve yalnızca doğum tarihi alanı ekledik ve
kullanıcımızın giriş yapması için username değil; sisteme kayıtlı email adresini 
kullanmasının yeterli olacağını söyledik. 

Bundan sonraki aşamada, kullanıcımızın davalarının tutulacağı Dava modelimizi de
oluşturacağız.
"""
class DavaKarsiTaraf(models.Model):
    davakarsitaraf_isim = models.CharField(max_length= 150)

    def __str__(self):
        return self.davakarsitaraf_isim

    class Meta:
        ordering = ('davakarsitaraf_isim',)
        verbose_name = ('Dava Karşı Taraf')
        verbose_name_plural = _('Dava Karşı Tarafları')

class Dava(models.Model):
    dava_title = models.CharField(('Dava Adı'), max_length=150)

    DAVA_CATEGORY_CHOICES = (
        ('Adli', 'Adli'),
        ('Ceza', 'Ceza'),
        ('İdari', 'İdari'),
        ('Tahkim', 'Tahkim'),
        ('Arabuluculuk', 'Arabuluculuk')
    )
    dava_category = models.CharField(('Dava Kategorisi'), max_length=30, choices=DAVA_CATEGORY_CHOICES, default='Kategori Belirtilmemiş')

    dava_esasno = models.CharField(('Dava Esas Numarası'), max_length=150, default='')
    DAVA_SIFAT_CHOICES = (
        ('Davacı', 'Davacı'),
        ('Davalı', 'Davalı')
    )

    dava_sifat = models.CharField(('Davadaki Sıfatımız'), max_length=50, default='', choices=DAVA_SIFAT_CHOICES)

    dava_mahkemeonad = models.CharField(('Mahkeme Adliye ve Numarası'), max_length=50, default='')

    DAVA_MAHKEME_CHOICES = (
        ('Asliye Hukuk Mahkemesi', 'Asliye Hukuk Mahkemesi'),
        ('Sulh Hukuk Mahkemesi', 'Sulh Hukuk Mahkemesi'),
        ('Aile Mahkemesi', 'Aile Mahkemesi'),
        ('İş Mahkemesi', 'İş Mahkemesi'),
        ('Ticaret Mahkemesi', 'Ticaret Mahkemesi'),
        ('İcra Mahkemesi', 'İcra Mahkemesi'),
        ('Tüketici Mahkemesi', 'Tüketici Mahkemesi'),
        ('Sulh Ceza Mahkemesi', 'Sulh Ceza Mahkemesi'),
        ('Asliye Ceza Mahkemesi', 'Asliye Ceza Mahkemesi'),
        ('Ağır Ceza Mahkemesi', 'Ağır Ceza Mahkemesi'),
        ('İcra Dairesi', 'İcra Dairesi'),
        ('İdare Mahkemesi', 'İdare Mahkemesi'),
        ('Vergi Mahkemesi', 'Vergi Mahkemesi')
    )

    dava_mahkeme = models.CharField(('Davanın Görüldüğü Mahkeme'), max_length=50, default='', choices=DAVA_MAHKEME_CHOICES)




    dava_description = models.TextField(('Dava Açıklaması'))
    dava_link = models.CharField(('Dava Dosyalarının Olduğu Link'), max_length=300)  ## Burada dava dosyamızın indirme linkini vereceğiz.
    dava_start = models.DateField(auto_now_add=True, blank=True)

    davakarsitaraf= models.ManyToManyField(DavaKarsiTaraf)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.dava_esasno + ' --- ' + str(self.user.all()[0])

    class Meta:
        ordering= ('-dava_start',)
        verbose_name = ('dava')
        verbose_name_plural = ('davalar')


"""
Yukarıda bir kullanıcının birden çok davası olabileceği ve bir davanın da müvekkili olarak birden çok kişinin vekili
olunabileceği için; User ile Dava modellerimiz arasında ManyToMany bir ilişki kurmuş olduk. Şimdi yukarıdaki Dava
modelimiz ile dava süreçlerini ManyToOne ile birbirine bağlayacağız ve her bir davamızda ne aşamalardan geçilmiş 
bu modelimizde yazdıracağız.
"""




class Surec(models.Model):
    surec_title = models.CharField(('Süreç Başlığı'), max_length=150)
    surec_description = models.TextField(('Süreç Açıklaması'))
    surec_date = models.DateField(('Süreç Zamanı'))  ## Surecimizin ne zaman oldugunu göstererek süreç sıralamasını sayfada surec_date'e göre yapacağız.

    dava = models.ForeignKey(Dava, on_delete=models.CASCADE)

    def __str__(self):
        return self.surec_title

    class Meta:
        ordering = ('-surec_date',)
        verbose_name = ('Dava Süreci')
        verbose_name_plural = ('Dava Süreçleri')

"""
Yukarıdaki şekilde de süreç verilerimizi dava verilerimiz ile birbirine bağlamış olduk.
"""


class Dosyalar(models.Model):
    dosya_adi = models.CharField(('Dosya Adı: '), max_length=60)
    dosya_aciklamasi = models.CharField(('Dosya Açıklaması: '), max_length= 150)
    dosya_dosyasi = models.FileField(('Gelen Dosya: '))

    dosya_gonderilme_tarihi = models.DateField(('Gönderilme Tarihi'), auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dava = models.ForeignKey(Dava, on_delete=models.CASCADE)

    def __str__(self):
        return self.dosya_adi

    class Meta:
        ordering = ('-dosya_gonderilme_tarihi',)
        verbose_name = ('Gönderilen Dosya')
        verbose_name_plural = ('Gönderilen Dosyalar')

@receiver(post_delete, sender=Dosyalar)
def submission_delete(sender, instance, **kwargs):
    instance.dosya_dosyasi.delete(False)
