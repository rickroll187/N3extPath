"""
Database Models for Talent Genome Service
Where talent data structures meet career genetics! 🧬📊
Built at 2025-08-03 18:22:04 UTC by the legendary genome master rickroll187
"""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TalentGenome(Base):
    """Model for talent genomes - the DNA sequence of careers! 🧬"""
    __tablename__ = "talent_genomes"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, unique=True, nullable=False, index=True)
    genome_version = Column(String(20), default="v4.0")
    overall_talent_score = Column(Float, nullable=False)  # 0-100 scale
    genetic_markers = Column(JSON, nullable=False)  # Key talent indicators
    skill_dna = Column(JSON, nullable=False)  # Skill proficiency mapping
    performance_genes = Column(JSON, nullable=False)  # Performance patterns
    learning_adaptability_score = Column(Float, nullable=False)  # How quickly they learn
    innovation_potential = Column(Float, nullable=False)  # Creative problem-solving ability
    collaboration_coefficient = Column(Float, nullable=False)  # Team synergy factor
    leadership_genome = Column(JSON, nullable=True)  # Leadership potential markers
    growth_trajectory = Column(String(20), nullable=False)  # ascending, stable, declining, variable
    career_velocity = Column(Float, nullable=False)  # Rate of career progression
    market_adaptability = Column(Float, nullable=False)  # Ability to adapt to market changes
    bias_score = Column(Float, default=0.0)  # Bias detection in analysis
    confidence_interval = Column(Float, default=0.85)  # Statistical confidence
    last_sequenced = Column(DateTime, default=datetime.utcnow)
    sequence_frequency_days = Column(Integer, default=90)  # How often to re-sequence
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trait_expressions = relationship("TalentTrait", back_populates="genome", cascade="all, delete-orphan")
    predictions = relationship("CareerPrediction", back_populates="genome", cascade="all, delete-orphan")
    comparisons = relationship("TalentComparison", back_populates="primary_genome", foreign_keys="TalentComparison.primary_genome_id")
    
    def __repr__(self):
        return f"<TalentGenome(employee_id={self.employee_id}, score={self.overall_talent_score}, trajectory='{self.growth_trajectory}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "genome_version": self.genome_version,
            "overall_talent_score": self.overall_talent_score,
            "genetic_markers": self.genetic_markers,
            "skill_dna": self.skill_dna,
            "performance_genes": self.performance_genes,
            "learning_adaptability_score": self.learning_adaptability_score,
            "innovation_potential": self.innovation_potential,
            "collaboration_coefficient": self.collaboration_coefficient,
            "leadership_genome": self.leadership_genome,
            "growth_trajectory": self.growth_trajectory,
            "career_velocity": self.career_velocity,
            "market_adaptability": self.market_adaptability,
            "bias_score": self.bias_score,
            "confidence_interval": self.confidence_interval,
            "last_sequenced": self.last_sequenced.isoformat(),
            "sequence_frequency_days": self.sequence_frequency_days,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class TalentTrait(Base):
    """Model for individual talent traits - the genetic building blocks! 🧬🔬"""
    __tablename__ = "talent_traits"
    
    id = Column(Integer, primary_key=True, index=True)
    genome_id = Column(Integer, ForeignKey('talent_genomes.id'), nullable=False)
    trait_name = Column(String(100), nullable=False)
    trait_category = Column(String(50), nullable=False)  # cognitive, behavioral, technical, soft
    expression_level = Column(Float, nullable=False)  # 0-100, how strongly this trait is expressed
    dominance = Column(String(20), nullable=False)  # dominant, recessive, co_dominant
    heritability = Column(Float, nullable=False)  # How likely this trait is to persist
    environmental_factors = Column(JSON, nullable=True)  # External factors affecting this trait
    development_potential = Column(Float, nullable=False)  # How much this trait can grow
    market_relevance = Column(Float, nullable=False)  # How valuable this trait is currently
    trait_interactions = Column(JSON, nullable=True)  # How this trait affects others
    measurement_confidence = Column(Float, default=0.85)  # Confidence in this measurement
    last_measured = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    genome = relationship("TalentGenome", back_populates="trait_expressions")
    
    def __repr__(self):
        return f"<TalentTrait(trait='{self.trait_name}', expression={self.expression_level}, dominance='{self.dominance}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "genome_id": self.genome_id,
            "trait_name": self.trait_name,
            "trait_category": self.trait_category,
            "expression_level": self.expression_level,
            "dominance": self.dominance,
            "heritability": self.heritability,
            "environmental_factors": self.environmental_factors,
            "development_potential": self.development_potential,
            "market_relevance": self.market_relevance,
            "trait_interactions": self.trait_interactions,
            "measurement_confidence": self.measurement_confidence,
            "last_measured": self.last_measured.isoformat()
        }

class CareerPrediction(Base):
    """Model for career trajectory predictions - the crystal ball of HR! 🔮"""
    __tablename__ = "career_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    genome_id = Column(Integer, ForeignKey('talent_genomes.id'), nullable=False)
    prediction_horizon_years = Column(Integer, nullable=False)
    predicted_roles = Column(JSON, nullable=False)  # Likely future roles
    success_probability = Column(Float, nullable=False)  # Likelihood of success
    growth_velocity = Column(Float, nullable=False)  # Rate of expected growth
    potential_salary_range = Column(JSON, nullable=True)  # Expected compensation range
    skill_evolution_path = Column(JSON, nullable=False)  # How skills will evolve
    leadership_emergence = Column(Float, nullable=False)  # Likelihood of leadership roles
    entrepreneurial_potential = Column(Float, nullable=False)  # Startup/innovation likelihood
    market_disruption_resilience = Column(Float, nullable=False)  # Adaptability to change
    career_satisfaction_forecast = Column(Float, nullable=False)  # Predicted job satisfaction
    risk_factors = Column(JSON, nullable=True)  # Potential career risks
    opportunity_indicators = Column(JSON, nullable=True)  # Growth opportunities
    prediction_algorithm = Column(String(50), default="neural_genetic_v4.0")
    confidence_score = Column(Float, nullable=False)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # When prediction becomes stale
    
    # Relationships
    genome = relationship("TalentGenome", back_populates="predictions")
    
    def to_dict(self):
        return {
            "id": self.id,
            "genome_id": self.genome_id,
            "prediction_horizon_years": self.prediction_horizon_years,
            "predicted_roles": self.predicted_roles,
            "success_probability": self.success_probability,
            "growth_velocity": self.growth_velocity,
            "potential_salary_range": self.potential_salary_range,
            "skill_evolution_path": self.skill_evolution_path,
            "leadership_emergence": self.leadership_emergence,
            "entrepreneurial_potential": self.entrepreneurial_potential,
            "market_disruption_resilience": self.market_disruption_resilience,
            "career_satisfaction_forecast": self.career_satisfaction_forecast,
            "risk_factors": self.risk_factors,
            "opportunity_indicators": self.opportunity_indicators,
            "prediction_algorithm": self.prediction_algorithm,
            "confidence_score": self.confidence_score,
            "prediction_date": self.prediction_date.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }

class TalentComparison(Base):
    """Model for talent genome comparisons - the genetic family tree of careers! 🌳"""
    __tablename__ = "talent_comparisons"
    
    id = Column(Integer, primary_key=True, index=True)
    primary_genome_id = Column(Integer, ForeignKey('talent_genomes.id'), nullable=False)
    comparison_genome_ids = Column(JSON, nullable=False)  # Other genomes in comparison
    comparison_criteria = Column(JSON, nullable=False)  # What was compared
    similarity_scores = Column(JSON, nullable=False)  # Similarity in different areas
    genetic_distance = Column(Float, nullable=False)  # Overall genetic distance
    shared_traits = Column(JSON, nullable=False)  # Common traits
    unique_traits = Column(JSON, nullable=False)  # Traits unique to primary genome
    competitive_advantages = Column(JSON, nullable=True)  # Where primary genome excels
    development_opportunities = Column(JSON, nullable=True)  # Where others excel
    peer_ranking = Column(Integer, nullable=True)  # Rank among compared genomes
    comparison_algorithm = Column(String(50), default="genetic_similarity_v4.0")
    statistical_significance = Column(Float, nullable=False)
    comparison_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    primary_genome = relationship("TalentGenome", back_populates="comparisons", foreign_keys=[primary_genome_id])
    
    def to_dict(self):
        return {
            "id": self.id,
            "primary_genome_id": self.primary_genome_id,
            "comparison_genome_ids": self.comparison_genome_ids,
            "comparison_criteria": self.comparison_criteria,
            "similarity_scores": self.similarity_scores,
            "genetic_distance": self.genetic_distance,
            "shared_traits": self.shared_traits,
            "unique_traits": self.unique_traits,
            "competitive_advantages": self.competitive_advantages,
            "development_opportunities": self.development_opportunities,
            "peer_ranking": self.peer_ranking,
            "comparison_algorithm": self.comparison_algorithm,
            "statistical_significance": self.statistical_significance,
            "comparison_date": self.comparison_date.isoformat()
        }

class SkillEvolution(Base):
    """Model for tracking skill evolution over time - the fossils of career development! 🦕"""
    __tablename__ = "skill_evolutions"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True, nullable=False)
    skill_name = Column(String(100), nullable=False)
    evolution_timeline = Column(JSON, nullable=False)  # Timeline of skill development
    growth_rate = Column(Float, nullable=False)  # Rate of skill improvement
    plateau_periods = Column(JSON, nullable=True)  # Periods of slow growth
    breakthrough_moments = Column(JSON, nullable=True)  # Significant improvement events
    decay_risk = Column(Float, nullable=False)  # Risk of skill degradation
    market_evolution_alignment = Column(Float, nullable=False)  # How skill evolves with market
    cross_pollination_effects = Column(JSON, nullable=True)  # How other skills affect this one
    future_relevance_score = Column(Float, nullable=False)  # How relevant skill will be
    investment_recommendation = Column(String(20), nullable=False)  # grow, maintain, pivot
    last_evolution_update = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "skill_name": self.skill_name,
            "evolution_timeline": self.evolution_timeline,
            "growth_rate": self.growth_rate,
            "plateau_periods": self.plateau_periods,
            "breakthrough_moments": self.breakthrough_moments,
            "decay_risk": self.decay_risk,
            "market_evolution_alignment": self.market_evolution_alignment,
            "cross_pollination_effects": self.cross_pollination_effects,
            "future_relevance_score": self.future_relevance_score,
            "investment_recommendation": self.investment_recommendation,
            "last_evolution_update": self.last_evolution_update.isoformat()
        }

class TalentBenchmark(Base):
    """Model for talent benchmarking - the genetic standards of excellence! 📏"""
    __tablename__ = "talent_benchmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    benchmark_name = Column(String(100), nullable=False)
    role_category = Column(String(50), nullable=False)
    experience_level = Column(String(20), nullable=False)  # junior, mid, senior, expert
    genetic_profile = Column(JSON, nullable=False)  # Expected genetic markers
    trait_thresholds = Column(JSON, nullable=False)  # Minimum trait levels
    performance_indicators = Column(JSON, nullable=False)  # Key performance metrics
    market_percentiles = Column(JSON, nullable=False)  # Market performance percentiles
    success_patterns = Column(JSON, nullable=False)  # Common success indicators
    sample_size = Column(Integer, nullable=False)  # Number of genomes in benchmark
    statistical_confidence = Column(Float, nullable=False)  # Confidence in benchmark
    benchmark_version = Column(String(20), default="v4.0")
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "benchmark_name": self.benchmark_name,
            "role_category": self.role_category,
            "experience_level": self.experience_level,
            "genetic_profile": self.genetic_profile,
            "trait_thresholds": self.trait_thresholds,
            "performance_indicators": self.performance_indicators,
            "market_percentiles": self.market_percentiles,
            "success_patterns": self.success_patterns,
            "sample_size": self.sample_size,
            "statistical_confidence": self.statistical_confidence,
            "benchmark_version": self.benchmark_version,
            "last_updated": self.last_updated.isoformat()
        }
