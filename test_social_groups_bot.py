import unittest

from analyzer import LeadAnalyzer
from config import GOOGLE_PLAY_URL
from sources.public_rss_monitor import PublicSocialRSSMonitor
from sources.webhook_server import normalize_webhook_payload
from sources.whatsapp_importer import parse_whatsapp_export_text


class TestSocialGroupsBot(unittest.TestCase):
    def test_google_play_url_present_in_all_mock_drafts(self):
        analyzer = LeadAnalyzer(api_key="")
        posts = PublicSocialRSSMonitor.get_mock_posts()
        self.assertEqual(len(posts), 6)
        for post in posts:
            lead_type, draft = analyzer.analyze(
                post["title"], post["content"], country=post["country"], platform=post["platform"]
            )
            self.assertIn(lead_type, ("SERVICE_SEEKER", "WORK_SEEKER"))
            self.assertIn(GOOGLE_PLAY_URL, draft)

    def test_whatsapp_export_parser_extracts_br_and_mx_leads(self):
        sample = (
            "22/11/2026 14:10 - Maria: Boa tarde grupo! Preciso de encanador urgente na Zona Sul.\n"
            "22/11/2026 14:12 - Pedro: Bom dia pessoal, tudo bem?\n"
            "[22/11/2026, 15:05:11] Carlos: Busco plomero en CDMX para fuga en cocina\n"
        )
        msgs = parse_whatsapp_export_text(sample, group_name="Servicos SP", country="BR")
        self.assertEqual(len(msgs), 3)
        self.assertEqual(msgs[0]["author"], "Maria")
        analyzer = LeadAnalyzer(api_key="")
        lt, draft = analyzer.analyze(msgs[0]["title"], msgs[0]["content"], country="BR", platform="whatsapp")
        self.assertEqual(lt, "SERVICE_SEEKER")
        self.assertIn("pl.serviceapp", draft)

    def test_webhook_normalization_for_whatsapp_facebook_tiktok(self):
        wpp = normalize_webhook_payload(
            "whatsapp",
            {"sender": "525512345678", "groupName": "Oficios CDMX", "pushName": "Juan", "text": "Busco electricista"},
        )
        self.assertEqual(wpp["platform"], "whatsapp")
        self.assertEqual(wpp["country"], "MX")

        fb = normalize_webhook_payload(
            "facebook",
            {"groupName": "Serviços SP", "author": "Ana", "text": "Indicação de diarista?", "url": "https://facebook.com/groups/1/posts/2"},
        )
        self.assertEqual(fb["platform"], "facebook")
        self.assertEqual(fb["country"], "BR")

        tt = normalize_webhook_payload(
            "tiktok",
            {"author": "@plomero_mty", "comment": "Ofrezco mis servicios de plomería en Monterrey", "url": "https://tiktok.com/@plomero_mty/video/1"},
        )
        self.assertEqual(tt["platform"], "tiktok")
        self.assertEqual(tt["country"], "MX")


if __name__ == "__main__":
    unittest.main()
