import random
from datetime import timedelta, date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = "Наполняет базу тестовыми данными"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Очищать существующие данные",
        )
        parser.add_argument(
            "--seed",
            action="store_true",
            help="Наполнять тестовыми данными",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Очищаю существующие данные...")
            self.clear_data()
        if options["seed"]:
            self.stdout.write("Создаю тестовые данные...")
            self.config = {
                "admin": {
                    "username": "admin",
                    "email": "admin@sports.com",
                    "password": "password123",
                    "first_name": "Админ",
                    "last_name": "Админов"
                },
                "trainers": [
                    {
                        "username": "trainer1",
                        "email": "trainer1@sports.com",
                        "password": "password123",
                        "first_name": "Иван",
                        "last_name": "Иванов"
                    },
                    {
                        "username": "trainer2",
                        "email": "trainer2@sports.com",
                        "password": "password123",
                        "first_name": "Мария",
                        "last_name": "Петрова"
                    },
                    {
                        "username": "trainer3",
                        "email": "trainer3@sports.com",
                        "password": "password123",
                        "first_name": "Алексей",
                        "last_name": "Сидоров"
                    }
                ],
                "sportsmen": [
                    {
                        "username": "sportsman1",
                        "email": "sportsman1@sports.com",
                        "password": "password123",
                        "first_name": "Дмитрий",
                        "last_name": "Кузнецов",
                        "birth_date": date(2000, 5, 15),
                        "razryad": "II взрослый"
                    },
                    {
                        "username": "sportsman2",
                        "email": "sportsman2@sports.com",
                        "password": "password123",
                        "first_name": "Анна",
                        "last_name": "Смирнова",
                        "birth_date": date(2001, 8, 22),
                        "razryad": "I взрослый"
                    },
                    {
                        "username": "sportsman3",
                        "email": "sportsman3@sports.com",
                        "password": "password123",
                        "first_name": "Сергей",
                        "last_name": "Васильев",
                        "birth_date": date(1999, 3, 10),
                        "razryad": "КМС"
                    },
                    {
                        "username": "sportsman4",
                        "email": "sportsman4@sports.com",
                        "password": "password123",
                        "first_name": "Елена",
                        "last_name": "Попова",
                        "birth_date": date(2002, 11, 5),
                        "razryad": "III взрослый"
                    },
                    {
                        "username": "sportsman5",
                        "email": "sportsman5@sports.com",
                        "password": "password123",
                        "first_name": "Андрей",
                        "last_name": "Новиков",
                        "birth_date": date(1998, 7, 30),
                        "razryad": "МС"
                    }
                ],
                "training_types": [
                    "Силовая тренировка",
                    "Кардио тренировка",
                    "Йога",
                    "Плавание",
                    "Стретчинг",
                    "Функциональный тренинг",
                    "Бокс",
                    "Кроссфит",
                    "Аэробика",
                    "Пилатес"
                ],
                "training_groups": [
                    {
                        "title": "Начинающие",
                        "description": "Группа для новичков, начальный уровень подготовки",
                        "is_active": True
                    },
                    {
                        "title": "Продвинутые",
                        "description": "Группа для опытных спортсменов",
                        "is_active": True
                    },
                    {
                        "title": "Профессионалы",
                        "description": "Элитная группа для участия в соревнованиях",
                        "is_active": True
                    }
                ],
                "exercises": [
                    "Приседания со штангой",
                    "Жим лежа",
                    "Становая тяга",
                    "Подтягивания",
                    "Отжимания",
                    "Планка",
                    "Бег на беговой дорожке",
                    "Велотренажер",
                    "Гиперэкстензия",
                    "Подъем ног в висе",
                    "Жим гантелей сидя",
                    "Разводка гантелей",
                    "Французский жим",
                    "Сгибания рук со штангой",
                    "Выпады с гантелями"
                ],
                "notifications": [
                    "Новая тренировка добавлена в расписание",
                    "Тренер оставил комментарий к вашей тренировке",
                    "Не забудьте подтвердить участие в завтрашней тренировке",
                    "Ваш прогресс за месяц: +5% к силовым показателям",
                    "Обновлено расписание на следующую неделю",
                    "Доступны новые тренировочные программы",
                    "Напоминание об оплате абонемента",
                    "Запланирована встреча с тренером",
                    "Ваша группа победила в соревнованиях!",
                    "Обновлены медицинские данные - проверьте профиль"
                ],
                "razryady": [
                    "III юношеский",
                    "II юношеский", 
                    "I юношеский",
                    "III взрослый",
                    "II взрослый",
                    "I взрослый",
                    "КМС",
                    "МС"
                ],
                "generation_settings": {
                    "trainings_count": 15,
                    "exercises_per_training_min": 4,
                    "exercises_per_training_max": 8,
                    "schedules_count": 20,
                    "notifications_per_user_min": 1,
                    "notifications_per_user_max": 5,
                    "training_types_per_trainer_min": 2,
                    "training_types_per_trainer_max": 4
                }
            }
            self.create_admin()
            trainer_users = self.create_trainer_users()
            sportsman_users = self.create_sportsman_users()
            training_types = self.create_training_types()
            groups = self.create_training_groups()
            trainers = self.create_trainer_profiles(trainer_users)
            sportsmen = self.create_sportsman_profiles(sportsman_users, trainers, groups)
            self.assign_training_types_to_trainers(trainers, training_types)
            schedules = self.create_schedules(trainers, training_types, sportsmen, groups)
            self.create_training_responses(schedules, sportsmen)
            trainings = self.create_trainings(trainers, training_types, groups)
            self.create_exercises(trainings, sportsman_users)
            self.create_notifications(trainer_users + sportsman_users)
            self.stdout.write(self.style.SUCCESS("✅ Тестовые данные успешно созданы!"))

    def clear_data(self):
        from training.models import Training, Exercise, ProgressLog
        from users.models import (
            Trainer, TrainingType, TrainingGroup, Sportsman, Schedule,
            TrainingResponse, TrainerTrainingType, Notification
        )
        ProgressLog.objects.all().delete()
        Exercise.objects.all().delete()
        Training.objects.all().delete()
        TrainingResponse.objects.all().delete()
        Schedule.objects.all().delete()
        TrainerTrainingType.objects.all().delete()
        Sportsman.objects.all().delete()
        Trainer.objects.all().delete()
        Notification.objects.all().delete()
        TrainingGroup.objects.all().delete()
        TrainingType.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(self.style.SUCCESS("Данные удалены"))

    def create_admin(self):
        admin_data = self.config["admin"]
        User.objects.create_superuser(
            username=admin_data["username"],
            email=admin_data["email"],
            password=admin_data["password"],
            first_name=admin_data["first_name"],
            last_name=admin_data["last_name"]
        )
        self.stdout.write(self.style.SUCCESS(f"Создан администратор: {admin_data['username']} / {admin_data['password']}"))

    def create_trainer_users(self):
        users = []
        for trainer_data in self.config["trainers"]:
            if not User.objects.filter(username=trainer_data["username"]).exists():
                user = User.objects.create_user(
                    username=trainer_data["username"],
                    email=trainer_data["email"],
                    password=trainer_data["password"],
                    first_name=trainer_data["first_name"],
                    last_name=trainer_data["last_name"],
                    is_staff=True
                )
                users.append(user)
                self.stdout.write(f"Создан пользователь тренера: {user.get_full_name()}")
        
        return users

    def create_sportsman_users(self):
        users = []
        for sportsman_data in self.config["sportsmen"]:
            if not User.objects.filter(username=sportsman_data["username"]).exists():
                user = User.objects.create_user(
                    username=sportsman_data["username"],
                    email=sportsman_data["email"],
                    password=sportsman_data["password"],
                    first_name=sportsman_data["first_name"],
                    last_name=sportsman_data["last_name"]
                )
                users.append(user)
                self.stdout.write(f"Создан пользователь спортсмена: {user.get_full_name()}")
        
        return users

    def create_training_types(self):
        from users.models import TrainingType

        training_types = []
        for type_name in self.config["training_types"]:
            training_type, created = TrainingType.objects.get_or_create(name=type_name)
            if created:
                training_types.append(training_type)
                self.stdout.write(f"Создан тип тренировки: {type_name}")

        return training_types

    def create_trainer_profiles(self, trainer_users):
        from users.models import Trainer

        trainers = []
        for user in trainer_users:
            trainer, created = Trainer.objects.get_or_create(
                user=user,
                defaults={'avatar': None}
            )
            if created:
                trainers.append(trainer)
                self.stdout.write(f"Создан профиль тренера: {trainer}")

        return trainers

    def create_training_groups(self):
        from users.models import TrainingGroup

        groups = []
        for group_data in self.config["training_groups"]:
            group, created = TrainingGroup.objects.get_or_create(
                title=group_data["title"],
                defaults={
                    'description': group_data["description"],
                    'is_active': group_data["is_active"]
                }
            )
            if created:
                groups.append(group)
                self.stdout.write(f"Создана группа: {group_data['title']}")

        return groups

    def create_sportsman_profiles(self, sportsman_users, trainers, groups):
        from users.models import Sportsman

        sportsmen = []
        
        for i, user in enumerate(sportsman_users):
            sportsman_data = self.config["sportsmen"][i]
            
            sportsman, created = Sportsman.objects.get_or_create(
                user=user,
                defaults={
                    'birth_date': sportsman_data["birth_date"],
                    'is_active': True,
                    'main_trainer': random.choice(trainers) if trainers else None,
                    'razryad': sportsman_data["razryad"],
                    'training_group': random.choice(groups) if groups else None,
                    'avatar': None
                }
            )
            if created:
                sportsmen.append(sportsman)
                self.stdout.write(f"Создан профиль спортсмена: {sportsman}")

        return sportsmen

    def assign_training_types_to_trainers(self, trainers, training_types):
        from users.models import TrainerTrainingType
        
        settings = self.config["generation_settings"]

        for trainer in trainers:
            num_types = random.randint(
                settings["training_types_per_trainer_min"],
                settings["training_types_per_trainer_max"]
            )
            selected_types = random.sample(
                training_types,
                min(num_types, len(training_types))
            )

            for training_type in selected_types:
                TrainerTrainingType.objects.get_or_create(
                    trainer=trainer,
                    training_type=training_type
                )

            self.stdout.write(f"Тренеру {trainer} назначены {len(selected_types)} типа(ов) тренировок")

    def create_schedules(self, trainers, training_types, sportsmen, groups):
        from users.models import Schedule

        schedules = []
        settings = self.config["generation_settings"]
        
        for i in range(settings["schedules_count"]):
            start_time = timezone.now() + timedelta(
                days=random.randint(0, 14),
                hours=random.randint(7, 20)
            )
            finish_time = start_time + timedelta(hours=1, minutes=30)

            training_type = random.choice(training_types)
            is_group = random.choice([True, False])

            schedule_data = {
                'training_type': training_type,
                'start_time': start_time,
                'finish_time': finish_time,
                'status': random.choice(['scheduled', 'scheduled', 'scheduled', 'completed']),
                'type': 'group' if is_group else 'individual',
                'description': f"Тренировка {i+1}. Важно принести сменную обувь.",
                'trainer': random.choice(trainers)
            }

            if is_group and groups:
                schedule_data['group'] = random.choice(groups)
                schedule_data['sportsman'] = None
            elif sportsmen:
                schedule_data['sportsman'] = random.choice(sportsmen)
                schedule_data['group'] = None

            schedule = Schedule.objects.create(**schedule_data)
            schedules.append(schedule)
            self.stdout.write(f"Создана тренировка в расписании: {schedule}")

        return schedules

    def create_training_responses(self, schedules, sportsmen):
        from users.models import TrainingResponse

        for schedule in schedules:
            if schedule.type == 'group' and schedule.group:
                group_sportsmen = [sportsman for sportsman in sportsmen if sportsman.training_group == schedule.group]
                for sportsman in group_sportsmen:
                    status = random.choice(['waiting', 'accepted', 'declined'])
                    TrainingResponse.objects.get_or_create(
                        schedule=schedule,
                        sportsman=sportsman,
                        defaults={'status': status}
                    )
            elif schedule.type == 'individual' and schedule.sportsman:
                status = random.choice(['accepted', 'declined'])
                TrainingResponse.objects.get_or_create(
                    schedule=schedule,
                    sportsman=schedule.sportsman,
                    defaults={'status': status}
                )

        self.stdout.write("Созданы ответы спортсменов на тренировки")

    def create_trainings(self, trainers, training_types, groups):
        from training.models import Training

        trainings = []
        settings = self.config["generation_settings"]
        
        for i in range(settings["trainings_count"]):
            training_type_obj = random.choice(training_types)
            group_obj = random.choice(groups) if groups and random.choice([True, False]) else None
            coach_user = random.choice([t.user for t in trainers]) if trainers else None

            training = Training.objects.create(
                title=f"Тренировочный план #{i+1}",
                training_type=training_type_obj,
                group=group_obj,
                coach=coach_user,
                date=timezone.now() + timedelta(days=random.randint(-30, 30)),
                duration_minutes=random.choice([60, 75, 90, 120]),
                notes=f"План тренировки {i+1}. Выполнять в указанном порядке."
            )
            trainings.append(training)
            self.stdout.write(f"Создан тренировочный план: {training}")

        return trainings

    def create_exercises(self, trainings, sportsman_users):
        from training.models import Exercise, ProgressLog
        
        settings = self.config["generation_settings"]

        for training in trainings:
            num_exercises = random.randint(
                settings["exercises_per_training_min"],
                settings["exercises_per_training_max"]
            )
            selected_exercises = random.sample(
                self.config["exercises"],
                min(num_exercises, len(self.config["exercises"]))
            )

            for order, exercise_name in enumerate(selected_exercises, 1):
                exercise = Exercise.objects.create(
                    training=training,
                    name=exercise_name,
                    description=f"Упражнение {order}: {exercise_name}",
                    order=order,
                    sets=random.randint(3, 5),
                    repetitions=random.choice(['10-12', '12-15', '8-10', '15-20', '30 сек']),
                    rest_seconds=random.choice([60, 90, 120, 180])
                )
                if random.choice([True, False]) and sportsman_users:
                    athlete = random.choice(sportsman_users)
                    ProgressLog.objects.create(
                        exercise=exercise,
                        athlete=athlete,
                        date=timezone.now() - timedelta(days=random.randint(1, 30)),
                        notes="Выполнено хорошо",
                        completed_sets=random.randint(1, exercise.sets),
                        actual_repetitions=exercise.repetitions,
                        weight_kg=random.uniform(10, 100)
                    )

            self.stdout.write(f"Для тренировки '{training.title}' создано {num_exercises} упражнений")

    def create_notifications(self, users):
        from users.models import Notification
        
        settings = self.config["generation_settings"]

        for user in users:
            num_notifications = random.randint(
                settings["notifications_per_user_min"],
                settings["notifications_per_user_max"]
            )

            for _ in range(num_notifications):
                Notification.objects.create(
                    user=user,
                    message=random.choice(self.config["notifications"]),
                    is_read=random.choice([True, False])
                )

        self.stdout.write(f"Созданы уведомления для {len(users)} пользователей")
