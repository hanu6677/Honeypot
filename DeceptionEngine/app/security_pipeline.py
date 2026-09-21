from .risk_engine import RiskEngine
from .report_generator import SecurityReportGenerator


class SecurityPipeline:

    def __init__(self):
        self.risk_engine = RiskEngine()
        self.report_generator = SecurityReportGenerator()
        self.events = []

    def add_event(self, event):
        if event:
            self.events.append(event)

    def analyze(self):
        return self.risk_engine.analyze(self.events)

    def finish_session(self, session):

        analysis = self.analyze()

        report_text, report_path = self.report_generator.generate(
            session=session,
            events=self.events,
            analysis=analysis
        )

        return {
            "analysis": analysis,
            "report": report_text,
            "report_path": report_path,
        }