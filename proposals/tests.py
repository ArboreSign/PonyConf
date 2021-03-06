from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase

from accounts.models import Participation

from .models import Talk, Topic, Vote


class ProposalsTests(TestCase):
    def setUp(self):
        a, b, c = (User.objects.create_user(guy, email='%s@example.org' % guy, password=guy) for guy in 'abc')
        Topic.objects.create(name='topipo', description='super topic', site=Site.objects.first())
        c.is_superuser = True
        c.save()

    def test_everything(self):
        # talk-edit
        self.client.login(username='a', password='a')
        self.client.post(reverse('add-talk'),
                         {'title': 'super talk',
                          'abstract': 'super',
                          'description': 'this is my super talk',
                          'notes': 'you can watch my previous talk videos',
                          'event': 1,
                          'topics': 1,
                          'speakers': 1})
        talk = Talk.objects.first()
        self.assertEqual(str(talk), 'super talk')
        self.assertEqual(talk.abstract, 'super')
        self.assertEqual(talk.description, 'this is my super talk')
        self.assertEqual(talk.notes, 'you can watch my previous talk videos')
        response = self.client.post(reverse('edit-talk', kwargs={'talk': 'super-talk'}),
                         {'title': 'mega talk', 'description': 'mega',
                          'event': 1, 'speakers': 1, 'duration': 60,
                          'registration_required': False, 'attendees_limit': 0})
        self.assertEqual(str(talk), 'super talk')  # title is read only there
        talk = Talk.objects.first()
        self.assertEqual(talk.description, 'mega')

        # Status Code
        for view in ['home', 'participate-as-speaker', 'add-talk', 'list-topics']:
            self.assertEqual(self.client.get(reverse(view)).status_code, 200)
        for view in ['list-talks', 'list-speakers']:
            self.assertEqual(self.client.get(reverse(view)).status_code, 403)
        self.assertEqual(self.client.get(reverse('list-speakers')).status_code, 403)
        self.assertEqual(self.client.get(reverse('edit-talk', kwargs={'talk': talk.slug})).status_code, 200)
        self.assertEqual(self.client.get(reverse('show-talk', kwargs={'slug': talk.slug})).status_code, 200)
        self.assertEqual(self.client.get(reverse('show-participant', kwargs={'username': 'a'})).status_code, 200)

        self.client.login(username='b', password='b')
        self.assertEqual(self.client.post(reverse('edit-talk', kwargs={'talk': 'super-talk'}),
                                          {'title': 'mega talk', 'description': 'mega', 'event': 1}).status_code, 403)
        self.assertEqual(self.client.get(reverse('participate-as-speaker')).status_code, 200)

        # Vote
        self.assertEqual(talk.score(), 0)
        self.assertEqual(self.client.get(reverse('vote', kwargs={'talk': talk.slug, 'score': 2})).status_code, 403)
        self.client.login(username='c', password='c')
        self.assertEqual(self.client.get(reverse('vote', kwargs={'talk': talk.slug, 'score': 2})).status_code, 302)
        self.assertEqual(talk.score(), 2)

        # Models str & get_asbolute_url
        for model in [Talk, Topic, Vote]:
            item = model.objects.first()
            self.assertEqual(self.client.get(item.get_absolute_url()).status_code, 200)
            self.assertTrue(str(item))

        # Talk.is_{editable,moderable}_by
        a, b, c = User.objects.all()
        self.assertTrue(talk.is_editable_by(c))  # c is superuser
        self.assertTrue(talk.is_moderable_by(c))  # c is superuser
        self.assertFalse(talk.is_editable_by(b))  # b is not speaker
        self.assertFalse(talk.is_moderable_by(b))  # b is not orga
        self.client.login(username='a', password='a')
        self.client.post(reverse('edit-talk', kwargs={'talk': 'super-talk'}),
                         {'title': 'mega talk', 'description': 'mega', 'event': 1,
                           'speakers': (a.pk, b.pk), 'duration': 60,
                          'registration_required': False, 'attendees_limit': 0})
        talk = Talk.objects.get(slug='super-talk')
        self.assertTrue(b in talk.speakers.all())
        self.assertTrue(talk.is_editable_by(b))  # b is speaker now
        self.assertFalse(talk.is_moderable_by(b))  # b is not orga

    def test_topic_edition_permissions(self):
        # Only orga and superuser can edit topics
        self.client.login(username='b', password='b')
        self.assertFalse(Participation.objects.get(user__username='b').orga)
        self.assertEqual(self.client.get(reverse('edit-topic', kwargs={'slug': 'topipo'})).status_code, 302)
        Participation.objects.filter(user__username='b').update(orga=True)
        self.assertEqual(self.client.get(reverse('edit-topic', kwargs={'slug': 'topipo'})).status_code, 200)
        self.client.login(username='c', password='c')  # superuser
        self.assertEqual(self.client.get(reverse('edit-topic', kwargs={'slug': 'topipo'})).status_code, 200)
        self.assertEqual(self.client.get(reverse('list-topics')).status_code, 200)
