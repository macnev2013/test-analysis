from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
import os


Base = declarative_base()


class TestResults(Base):
    __tablename__ = 'TestResults'

    id = Column(Integer, primary_key=True)
    project = Column(String)
    test_run_id = Column(Float)
    test_name = Column(String)
    test_result = Column(String)
    test_file_name = Column(String)
    duration = Column(Float)
    reason = Column(String)
    __table_args__ = (
        UniqueConstraint('test_run_id', 'test_file_name', 'test_name', 'project', name='_per_run_uc'),
     )

    def __repr__(self):
        return f"<TestResults(project={self.project}, test_run_id={self.test_run_id}, test_name={self.test_name}, test_result={self.test_result}, test_file_name={self.test_file_name}, duration={self.duration}>"