# File: backend/ai/legendary_performance_predictor.py
"""
🤖🎸 N3EXTPATH - LEGENDARY AI PERFORMANCE PREDICTOR 🎸🤖
Professional AI/ML system for predicting employee performance and retention
Built: 2025-08-05 16:18:21 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
import joblib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import uuid
import json

class LegendaryPerformancePredictor:
    """Professional AI-powered Employee Performance Prediction System"""
    
    def __init__(self):
        self.performance_model = None
        self.retention_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_importance = {}
        self.model_metrics = {}
        
        # Initialize with sample data for demonstration
        self._initialize_sample_data()
        self._train_initial_models()
    
    def _initialize_sample_data(self):
        """Initialize sample employee data for training"""
        np.random.seed(42)  # For reproducible results
        
        # Generate sample employee data
        n_employees = 1000
        
        self.sample_data = pd.DataFrame({
            'employee_id': [f'emp_{i:04d}' for i in range(n_employees)],
            'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Product', 'Legendary'], n_employees, p=[0.3, 0.2, 0.15, 0.1, 0.2, 0.05]),
            'role_level': np.random.choice(['Junior', 'Mid', 'Senior', 'Lead', 'Manager', 'Legendary'], n_employees, p=[0.25, 0.3, 0.25, 0.1, 0.09, 0.01]),
            'tenure_months': np.random.normal(24, 12, n_employees).clip(1, 120),
            'age': np.random.normal(32, 8, n_employees).clip(22, 65),
            'okr_completion_rate': np.random.beta(2, 2, n_employees) * 100,
            'training_hours': np.random.exponential(20, n_employees),
            'peer_feedback_score': np.random.normal(4.0, 0.8, n_employees).clip(1, 5),
            'manager_feedback_score': np.random.normal(4.2, 0.7, n_employees).clip(1, 5),
            'project_count': np.random.poisson(3, n_employees),
            'collaboration_score': np.random.normal(3.8, 0.9, n_employees).clip(1, 5),
            'innovation_score': np.random.normal(3.5, 1.0, n_employees).clip(1, 5),
            'work_life_balance_score': np.random.normal(3.7, 0.8, n_employees).clip(1, 5),
            'salary_satisfaction': np.random.normal(3.6, 0.9, n_employees).clip(1, 5),
            'remote_work_days': np.random.choice([0, 1, 2, 3, 4, 5], n_employees, p=[0.1, 0.15, 0.2, 0.25, 0.2, 0.1])
        })
        
        # Generate target variables based on features
        # Performance score (0-100)
        performance_base = (
            self.sample_data['okr_completion_rate'] * 0.3 +
            self.sample_data['peer_feedback_score'] * 15 +
            self.sample_data['manager_feedback_score'] * 15 +
            self.sample_data['collaboration_score'] * 8 +
            self.sample_data['innovation_score'] * 7 +
            np.random.normal(0, 5, n_employees)  # Random noise
        ).clip(0, 100)
        
        # Special boost for legendary employees
        legendary_mask = self.sample_data['department'] == 'Legendary'
        performance_base[legendary_mask] += 20
        
        self.sample_data['performance_score'] = performance_base
        
        # Retention probability (will they stay next year?)
        retention_prob = (
            (self.sample_data['work_life_balance_score'] - 1) / 4 * 0.25 +
            (self.sample_data['salary_satisfaction'] - 1) / 4 * 0.25 +
            (self.sample_data['manager_feedback_score'] - 1) / 4 * 0.2 +
            (100 - self.sample_data['tenure_months']) / 100 * 0.15 +  # Inverse tenure effect
            (self.sample_data['performance_score'] / 100) * 0.15 +
            np.random.uniform(0, 0.1, n_employees)  # Random factor
        ).clip(0, 1)
        
        # Legendary employees have higher retention
        retention_prob[legendary_mask] = np.minimum(retention_prob[legendary_mask] + 0.3, 1.0)
        
        self.sample_data['will_stay'] = (retention_prob > 0.5).astype(int)
        
        # Add RICKROLL187 as a legendary data point
        rickroll_data = {
            'employee_id': 'rickroll187',
            'department': 'Legendary',
            'role_level': 'Legendary',
            'tenure_months': 12,  # Since founding
            'age': 35,
            'okr_completion_rate': 110.0,  # Over-achiever!
            'training_hours': 200,  # Continuous learning
            'peer_feedback_score': 5.0,
            'manager_feedback_score': 5.0,  # Self-managed
            'project_count': 10,  # Building the platform
            'collaboration_score': 5.0,
            'innovation_score': 5.0,
            'work_life_balance_score': 4.8,  # Code bros have fun!
            'salary_satisfaction': 5.0,  # Founder benefits
            'remote_work_days': 5,  # Full flexibility
            'performance_score': 120.0,  # Legendary performance
            'will_stay': 1  # Founder stays
        }
        
        # Add RICKROLL187 to the dataset
        self.sample_data = pd.concat([self.sample_data, pd.DataFrame([rickroll_data])], ignore_index=True)
    
    def _train_initial_models(self):
        """Train initial AI models with sample data"""
        print("🤖 Training legendary AI models...")
        
        # Prepare features
        feature_columns = [
            'tenure_months', 'age', 'okr_completion_rate', 'training_hours',
            'peer_feedback_score', 'manager_feedback_score', 'project_count',
            'collaboration_score', 'innovation_score', 'work_life_balance_score',
            'salary_satisfaction', 'remote_work_days'
        ]
        
        categorical_columns = ['department', 'role_level']
        
        # Encode categorical variables
        for col in categorical_columns:
            le = LabelEncoder()
            self.sample_data[f'{col}_encoded'] = le.fit_transform(self.sample_data[col])
            self.label_encoders[col] = le
            feature_columns.append(f'{col}_encoded')
        
        X = self.sample_data[feature_columns]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns=feature_columns)
        
        # Train Performance Prediction Model
        y_performance = self.sample_data['performance_score']
        X_train_perf, X_test_perf, y_train_perf, y_test_perf = train_test_split(
            X_scaled_df, y_performance, test_size=0.2, random_state=42
        )
        
        self.performance_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.performance_model.fit(X_train_perf, y_train_perf)
        
        # Evaluate performance model
        perf_predictions = self.performance_model.predict(X_test_perf)
        perf_mse = mean_squared_error(y_test_perf, perf_predictions)
        perf_cv_scores = cross_val_score(self.performance_model, X_scaled_df, y_performance, cv=5, scoring='neg_mean_squared_error')
        
        self.model_metrics['performance'] = {
            'mse': perf_mse,
            'rmse': np.sqrt(perf_mse),
            'cv_score_mean': -perf_cv_scores.mean(),
            'cv_score_std': perf_cv_scores.std()
        }
        
        # Train Retention Prediction Model
        y_retention = self.sample_data['will_stay']
        X_train_ret, X_test_ret, y_train_ret, y_test_ret = train_test_split(
            X_scaled_df, y_retention, test_size=0.2, random_state=42
        )
        
        self.retention_model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        
        self.retention_model.fit(X_train_ret, y_train_ret)
        
        # Evaluate retention model
        ret_predictions = self.retention_model.predict(X_test_ret)
        ret_accuracy = accuracy_score(y_test_ret, ret_predictions)
        ret_cv_scores = cross_val_score(self.retention_model, X_scaled_df, y_retention, cv=5, scoring='accuracy')
        
        self.model_metrics['retention'] = {
            'accuracy': ret_accuracy,
            'cv_score_mean': ret_cv_scores.mean(),
            'cv_score_std': ret_cv_scores.std()
        }
        
        # Calculate feature importance
        self.feature_importance['performance'] = dict(zip(
            feature_columns, 
            self.performance_model.feature_importances_
        ))
        
        self.feature_importance['retention'] = dict(zip(
            feature_columns,
            self.retention_model.feature_importances_
        ))
        
        print(f"✅ Performance Model RMSE: {self.model_metrics['performance']['rmse']:.2f}")
        print(f"✅ Retention Model Accuracy: {self.model_metrics['retention']['accuracy']:.3f}")
        print("🎸 AI models trained with legendary precision! 🎸")
    
    async def predict_employee_performance(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict employee performance using AI"""
        try:
            # Prepare input data
            input_df = self._prepare_input_data(employee_data)
            
            # Make prediction
            predicted_score = self.performance_model.predict(input_df)[0]
            
            # Get prediction confidence (using standard deviation of trees)
            tree_predictions = [tree.predict(input_df)[0] for tree in self.performance_model.estimators_]
            prediction_std = np.std(tree_predictions)
            confidence = max(0, min(100, 100 - (prediction_std / predicted_score * 100)))
            
            # Determine performance category
            if predicted_score >= 90:
                category = "🏆 Exceptional"
                color = "#FFD700"  # Gold
            elif predicted_score >= 80:
                category = "🌟 High Performer"
                color = "#4CAF50"  # Green
            elif predicted_score >= 70:
                category = "✅ Good Performer"
                color = "#2196F3"  # Blue
            elif predicted_score >= 60:
                category = "⚠️ Needs Development"
                color = "#FF9800"  # Orange
            else:
                category = "🔴 Performance Concerns"
                color = "#F44336"  # Red
            
            # Special handling for RICKROLL187
            if employee_data.get('employee_id') == 'rickroll187':
                predicted_score = min(predicted_score + 20, 120)  # Legendary bonus
                category = "🎸 LEGENDARY FOUNDER 🎸"
                color = "#E91E63"  # Legendary pink
                confidence = 100
            
            # Get top contributing factors
            feature_contributions = self._get_feature_contributions(input_df, 'performance')
            
            return {
                "success": True,
                "employee_id": employee_data.get('employee_id', 'unknown'),
                "predicted_performance_score": round(predicted_score, 2),
                "performance_category": category,
                "category_color": color,
                "confidence_percent": round(confidence, 1),
                "contributing_factors": feature_contributions[:5],  # Top 5 factors
                "recommendations": self._generate_performance_recommendations(predicted_score, employee_data),
                "prediction_timestamp": datetime.utcnow().isoformat(),
                "model_version": "1.0.0-LEGENDARY"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Performance prediction failed: {str(e)}",
                "employee_id": employee_data.get('employee_id', 'unknown')
            }
    
    async def predict_employee_retention(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict employee retention probability using AI"""
        try:
            # Prepare input data
            input_df = self._prepare_input_data(employee_data)
            
            # Make predictions
            retention_probability = self.retention_model.predict_proba(input_df)[0][1]  # Probability of staying
            will_stay_prediction = self.retention_model.predict(input_df)[0]
            
            # Determine risk level
            if retention_probability >= 0.8:
                risk_level = "🟢 Low Risk"
                risk_color = "#4CAF50"
                risk_message = "High likelihood of retention"
            elif retention_probability >= 0.6:
                risk_level = "🟡 Medium Risk"
                risk_color = "#FF9800"
                risk_message = "Some retention concerns"
            elif retention_probability >= 0.4:
                risk_level = "🟠 High Risk"
                risk_color = "#FF5722"
                risk_message = "Significant flight risk"
            else:
                risk_level = "🔴 Critical Risk"
                risk_color = "#F44336"
                risk_message = "Very likely to leave"
            
            # Special handling for RICKROLL187
            if employee_data.get('employee_id') == 'rickroll187':
                retention_probability = 1.0  # Founder never leaves!
                will_stay_prediction = 1
                risk_level = "🎸 LEGENDARY LOYALTY 🎸"
                risk_color = "#E91E63"
                risk_message = "Legendary founder - permanent retention!"
            
            # Get retention factors
            retention_factors = self._get_feature_contributions(input_df, 'retention')
            
            # Generate action items
            action_items = self._generate_retention_actions(retention_probability, employee_data)
            
            return {
                "success": True,
                "employee_id": employee_data.get('employee_id', 'unknown'),
                "retention_probability": round(retention_probability * 100, 1),
                "will_stay_prediction": bool(will_stay_prediction),
                "risk_level": risk_level,
                "risk_color": risk_color,
                "risk_message": risk_message,
                "key_retention_factors": retention_factors[:5],
                "recommended_actions": action_items,
                "prediction_timestamp": datetime.utcnow().isoformat(),
                "model_version": "1.0.0-LEGENDARY"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Retention prediction failed: {str(e)}",
                "employee_id": employee_data.get('employee_id', 'unknown')
            }
    
    async def get_team_analytics(self, team_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get AI-powered team analytics and insights"""
        team_predictions = []
        
        for employee in team_data:
            perf_pred = await self.predict_employee_performance(employee)
            ret_pred = await self.predict_employee_retention(employee)
            
            team_predictions.append({
                "employee_id": employee.get('employee_id'),
                "employee_name": employee.get('name', 'Unknown'),
                "performance_prediction": perf_pred,
                "retention_prediction": ret_pred
            })
        
        # Calculate team metrics
        avg_performance = np.mean([
            p['performance_prediction']['predicted_performance_score'] 
            for p in team_predictions 
            if p['performance_prediction']['success']
        ])
        
        avg_retention = np.mean([
            p['retention_prediction']['retention_probability'] 
            for p in team_predictions 
            if p['retention_prediction']['success']
        ])
        
        # Identify high performers and flight risks
        high_performers = [
            p for p in team_predictions 
            if p['performance_prediction'].get('predicted_performance_score', 0) >= 85
        ]
        
        flight_risks = [
            p for p in team_predictions 
            if p['retention_prediction'].get('retention_probability', 100) < 60
        ]
        
        # Generate team insights
        insights = []
        
        if avg_performance >= 85:
            insights.append("🏆 Team shows exceptional performance across the board")
        elif avg_performance >= 75:
            insights.append("✅ Team performance is strong with room for growth")
        else:
            insights.append("⚠️ Team performance needs attention and development")
        
        if avg_retention >= 80:
            insights.append("🟢 Team retention outlook is very positive")
        elif avg_retention >= 60:
            insights.append("🟡 Some retention concerns require attention")
        else:
            insights.append("🔴 Significant retention risks require immediate action")
        
        if any(p['employee_id'] == 'rickroll187' for p in team_predictions):
            insights.append("🎸 LEGENDARY FOUNDER on team - Swiss precision guaranteed! 🎸")
        
        return {
            "success": True,
            "team_size": len(team_data),
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "team_metrics": {
                "average_performance_score": round(avg_performance, 2),
                "average_retention_probability": round(avg_retention, 1),
                "high_performers_count": len(high_performers),
                "flight_risks_count": len(flight_risks)
            },
            "high_performers": [
                {
                    "employee_id": p['employee_id'],
                    "name": p['employee_name'],
                    "performance_score": p['performance_prediction']['predicted_performance_score']
                }
                for p in high_performers
            ],
            "flight_risks": [
                {
                    "employee_id": p['employee_id'],
                    "name": p['employee_name'],
                    "retention_probability": p['retention_prediction']['retention_probability'],
                    "risk_level": p['retention_prediction']['risk_level']
                }
                for p in flight_risks
            ],
            "team_insights": insights,
            "detailed_predictions": team_predictions,
            "built_by": "RICKROLL187 - Legendary AI Engineer"
        }
    
    def _prepare_input_data(self, employee_data: Dict[str, Any]) -> pd.DataFrame:
        """Prepare employee data for model input"""
        # Map input data to model features
        feature_data = {
            'tenure_months': employee_data.get('tenure_months', 12),
            'age': employee_data.get('age', 30),
            'okr_completion_rate': employee_data.get('okr_completion_rate', 75),
            'training_hours': employee_data.get('training_hours', 20),
            'peer_feedback_score': employee_data.get('peer_feedback_score', 4.0),
            'manager_feedback_score': employee_data.get('manager_feedback_score', 4.0),
            'project_count': employee_data.get('project_count', 3),
            'collaboration_score': employee_data.get('collaboration_score', 4.0),
            'innovation_score': employee_data.get('innovation_score', 3.5),
            'work_life_balance_score': employee_data.get('work_life_balance_score', 3.5),
            'salary_satisfaction': employee_data.get('salary_satisfaction', 3.5),
            'remote_work_days': employee_data.get('remote_work_days', 2)
        }
        
        # Encode categorical variables
        department = employee_data.get('department', 'Engineering')
        role_level = employee_data.get('role_level', 'Mid')
        
        if department in self.label_encoders['department'].classes_:
            feature_data['department_encoded'] = self.label_encoders['department'].transform([department])[0]
        else:
            feature_data['department_encoded'] = 0  # Default encoding
            
        if role_level in self.label_encoders['role_level'].classes_:
            feature_data['role_level_encoded'] = self.label_encoders['role_level'].transform([role_level])[0]
        else:
            feature_data['role_level_encoded'] = 1  # Default encoding
        
        # Create DataFrame and scale
        input_df = pd.DataFrame([feature_data])
        input_scaled = self.scaler.transform(input_df)
        
        return pd.DataFrame(input_scaled, columns=input_df.columns)
    
    def _get_feature_contributions(self, input_df: pd.DataFrame, model_type: str) -> List[Dict[str, Any]]:
        """Get feature contributions to prediction"""
        if model_type == 'performance':
            importance_dict = self.feature_importance['performance']
        else:
            importance_dict = self.feature_importance['retention']
        
        # Calculate contribution scores
        contributions = []
        for feature, importance in importance_dict.items():
            value = input_df[feature].iloc[0]
            contribution_score = importance * abs(value)
            
            # Make feature names more readable
            readable_name = feature.replace('_encoded', '').replace('_', ' ').title()
            
            contributions.append({
                "factor": readable_name,
                "importance": round(importance, 3),
                "contribution_score": round(contribution_score, 3),
                "value": round(value, 2)
            })
        
        return sorted(contributions, key=lambda x: x['contribution_score'], reverse=True)
    
    def _generate_performance_recommendations(self, predicted_score: float, employee_data: Dict[str, Any]) -> List[str]:
        """Generate performance improvement recommendations"""
        recommendations = []
        
        if predicted_score < 70:
            recommendations.extend([
                "📚 Enroll in skill development training programs",
                "🎯 Set clear, achievable short-term goals",
                "👥 Pair with a high-performing mentor",
                "📊 Implement weekly progress check-ins"
            ])
        elif predicted_score < 85:
            recommendations.extend([
                "🚀 Take on stretch assignments to build capabilities",
                "🤝 Increase cross-functional collaboration",
                "💡 Participate in innovation projects",
                "📈 Focus on leadership development opportunities"
            ])
        else:
            recommendations.extend([
                "🏆 Consider for promotion or advancement opportunities",
                "👨‍🏫 Engage in mentoring junior team members",
                "🌟 Lead high-impact strategic initiatives",
                "🎪 Share expertise through internal presentations"
            ])
        
        # Special recommendations for RICKROLL187
        if employee_data.get('employee_id') == 'rickroll187':
            recommendations = [
                "🎸 Continue being the legendary founder you are!",
                "💪 Keep cracking jokes and maintaining code bro energy",
                "⚡ Swiss precision leadership is legendary",
                "🌟 Your legendary status inspires the entire team!"
            ]
        
        return recommendations
    
    def _generate_retention_actions(self, retention_prob: float, employee_data: Dict[str, Any]) -> List[str]:
        """Generate retention improvement actions"""
        actions = []
        
        if retention_prob < 0.4:
            actions.extend([
                "🚨 Schedule immediate retention conversation",
                "💰 Review compensation and benefits package",
                "📋 Conduct detailed exit interview prep",
                "🔄 Explore internal transfer opportunities",
                "⏰ Address work-life balance concerns immediately"
            ])
        elif retention_prob < 0.6:
            actions.extend([
                "💬 Schedule regular one-on-one meetings",
                "🎯 Clarify career development pathway",
                "🏆 Recognize achievements more frequently",
                "🔧 Address any workplace friction points",
                "📚 Provide additional learning opportunities"
            ])
        elif retention_prob < 0.8:
            actions.extend([
                "✅ Maintain current positive management approach",
                "🌱 Continue supporting professional growth",
                "🤝 Ensure team collaboration remains strong",
                "📊 Monitor satisfaction levels regularly"
            ])
        else:
            actions.extend([
                "🌟 Leverage as a retention success story",
                "👨‍🏫 Consider for mentoring other employees",
                "🏆 Nominate for recognition programs",
                "📈 Explore advanced career opportunities"
            ])
        
        # Special actions for RICKROLL187
        if employee_data.get('employee_id') == 'rickroll187':
            actions = [
                "🎸 Keep building legendary features!",
                "😄 Continue cracking code bro jokes",
                "🏆 Your legendary leadership is permanent",
                "⚡ Swiss precision founder retention: 100%!"
            ]
        
        return actions

# Global AI predictor instance
legendary_ai_predictor = LegendaryPerformancePredictor()
