import inspect
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
from taggit.managers import TaggableManager
from faker import Factory
from random import randint, sample
from blog.models import Post, Category


class Command(BaseCommand):
    def fake_markdown_content(self, faker):
        sumup = ''
        for i in range(randint(1, 3)):
            header = '# {0}    \n'.format(faker.sentence(nb_words=3))
            subheader = '## {0}    \n'.format(faker.word())
            content = '\n'.join(faker.paragraphs(nb=2)) + '    \n' + \
                '    \n```\n{0}```      \n'.format(
                inspect.getsource(sample([
                                         self.fake_markdown_content,
                                         self.handle,
                                         randint,
                                         sample
                                         ], 1)[0]))
            sumup += header + subheader + content
        return sumup

    def handle(self, *args, **options):
        self.stdout.write('wait a second..')
        fake = Factory.create('zh_CN')
        iamge_base = settings.QINIU_BASE_URL + 'fake_site/'

        for i in range(1, 4):
            c = Category(id=i, name='test category {0}'.format(i))
            c.save()

        tags = []
        for i in range(20):
            tags.append(fake.city())
        tags = set(tags)

        for i in range(50):
            p = Post(category=Category.objects.get(pk=randint(1, 3)),
                     header_image_url=iamge_base + '{}.jpg'.format(randint(1, 5)),
                     title=fake.country() + fake.city_name() + fake.street_name(),
                     subtitle=fake.sentence(nb_words=2, variable_nb_words=True),
                     content=self.fake_markdown_content(fake))

            p.save()
            p.tags.add(*sample(tags, randint(1, 3)))
            orginal = p.create_date
            p.create_date = orginal.replace(year=randint(2013, 2015),
                                            month=randint(1, 12))
            p.save()

        user = User.objects.create_user('demouser', password='demouser')
        user.save()

        self.stdout.write(self.style.SUCCESS('done!'))
        self.stdout.write(self.style.SUCCESS('username as password: demouser'))
