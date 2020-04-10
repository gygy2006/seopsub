import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from posts import models as post_models
from users import models as user_models


class Command(BaseCommand):
    help = "This command creates many posts"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many posts do you want to posts"
        )

    def handele(self, *args, **options):
        print(options)
        number = options.get("number")
        seeder = Seed.seeder()
        all_usres = user_models.User.objects.all()
        all_category = post_models.Category.objects.all()
        seeder.add_entity(
            post_models.Post,
            number,
            {
                "title" : lambda x: seeder.faker.address(),
                "summary" : lambda x: seeder.faker.company(),
                "author" : lambda x: random.choice(all_usres),
                "category" : lambda x: random.choice(all_category)
            }
        )

        created_body = seeder.excute()
        created_clean = flatten(list(created_body.values()))
        for pk in created_clean:
            post = post_models.Post.objects.get(pk=pk)
            