"""
interview_data.py — Interview Question Database
===============================================
Curated Q&A content for data roles, categorized by difficulty.
Expanded to include Data Scientist, Data Analyst, Data Engineer, and ML Engineer.
"""

import random

INTERVIEW_DB = {
    "Data Scientist": {
        "Easy": [
            {"question": "What is the difference between supervised and unsupervised learning?", "answer": "Supervised learning uses labeled data for prediction; unsupervised finds patterns in unlabeled data."},
            {"question": "What is Overfitting?", "answer": "When a model learns noise in training data, hurting its performance on new data."},
            {"question": "Define 'Mean' and 'Median'. When is Median better?", "answer": "Mean is average; Median is the middle value. Median is better with skewed data or outliers."},
            {"question": "What is a p-value?", "answer": "The probability of results being due to chance. Usually < 0.05 is significant."},
            {"question": "What is the Purpose of Data Normalization?", "answer": "To scale features to a similar range, preventing one feature from dominating the model."},
            {"question": "What is a Confusion Matrix?", "answer": "A table used to describe the performance of a classification model."},
            {"question": "Explain 'R-squared'.", "answer": "A statistical measure of how close the data are to the fitted regression line."},
            {"question": "What are Outliers?", "answer": "Data points that differ significantly from other observations."},
            {"question": "What is the difference between L1 and L2 regularization?", "answer": "L1 (Lasso) can shrink coefficients to zero; L2 (Ridge) shrinks them but not to zero."},
            {"question": "What is Cross-Validation?", "answer": "A technique to evaluate model performance by partitioning data into subsets."}
        ],
        "Medium": [
            {"question": "Explain the Bias-Variance tradeoff.", "answer": "Bias is error from assumptions; Variance is sensitivity to data fluctuations. Balance is key."},
            {"question": "How do you handle missing data?", "answer": "Deletion, Imputation (Mean/Median), or using robust models like Random Forest."},
            {"question": "What is the 'Curse of Dimensionality'?", "answer": "As features increase, the amount of data needed grows exponentially and data becomes sparse."},
            {"question": "How does a Random Forest work?", "answer": "An ensemble of decision trees, usually trained with 'bagging' to reduce variance."},
            {"question": "Explain Logistic Regression.", "answer": "A classification algorithm that predicts probabilities using a sigmoid function."},
            {"question": "What is Gradient Descent?", "answer": "An optimization algorithm used to minimize a loss function iteratively."},
            {"question": "Difference between Precision and Recall?", "answer": "Precision: correct positives / all predicted positives. Recall: correct positives / all actual positives."},
            {"question": "What is A/B Testing?", "answer": "A statistical way to compare two versions of a variable to determine which performs better."},
            {"question": "How do you treat imbalanced datasets?", "answer": "Oversampling (SMOTE), Undersampling, or using specific metrics like F1-score/AUC-ROC."},
            {"question": "What is Principal Component Analysis (PCA)?", "answer": "A dimensionality reduction technique that transforms variables into uncorrelated principal components."}
        ],
        "Hard": [
            {"question": "Explain the 'Kernel Trick' in SVM.", "answer": "Implicitly maps data to high-dimensional space to find non-linear decision boundaries efficiently."},
            {"question": "How does XGBoost differ from Gradient Boosting?", "answer": "It uses second-order Taylor expansion for the loss function and has built-in regularization."},
            {"question": "Explain the architecture of a CNN.", "answer": "Convolutional layers (feature extraction), Pooling (downsampling), and Fully Connected layers."},
            {"question": "What is Backpropagation?", "answer": "The primary algorithm for training neural networks by calculating gradients of the loss function via the chain rule."},
            {"question": "Difference between Bagging and Boosting?", "answer": "Bagging builds trees in parallel (averaging); Boosting builds them sequentially (learning from errors)."},
            {"question": "What is the Vanishing Gradient problem?", "answer": "In deep networks, gradients become extremely small during backprop, preventing weights from changing."},
            {"question": "Explain 'Attention' in Deep Learning.", "answer": "A mechanism that allows models to focus on specific parts of the input sequence (e.g., in Transformers)."},
            {"question": "How do you determine the 'k' in K-Means?", "answer": "Elbow Method, Silhouette Score, or Gap Statistic."},
            {"question": "Explain Reinforcement Learning.", "answer": "Learning through trial and error by interacting with an environment to maximize rewards."},
            {"question": "What is an Autoencoder?", "answer": "A type of neural network used to learn efficient data codings in an unsupervised manner."}
        ]
    },
    "Data Analyst": {
        "Easy": [
            {"question": "What is a SQL JOIN?", "answer": "Combines rows from tables based on a related column."},
            {"question": "Difference between WHERE and HAVING in SQL?", "answer": "WHERE filters before aggregation; HAVING filters groups after aggregation."},
            {"question": "What are common types of data visualizations?", "answer": "Bar charts, Line graphs, Scatter plots, Pie charts, Heatmaps."},
            {"question": "Define 'Correlation'.", "answer": "A statistical relationship between two variables."},
            {"question": "What is Data Cleaning?", "answer": "Fixing or removing incorrect, corrupted, or incomplete data."},
            {"question": "Explain 'Standard Deviation'.", "answer": "Measure of variation or dispersion in a set of values."},
            {"question": "What is a Pivot Table?", "answer": "Summarize, sort, and group data in a spreadsheet."},
            {"question": "Qualitative vs. Quantitative data?", "answer": "Qualitative is descriptive; Quantitative is numerical."},
            {"question": "What is a Primary Key?", "answer": "Unique identifier for a record in a table."},
            {"question": "Excel vs. SQL?", "answer": "Excel for small data/manual; SQL for large data/retrieval."}
        ],
        "Medium": [
            {"question": "Explain Window Functions in SQL.", "answer": "Calculations across related rows (e.g., RANK, SUM OVER)."},
            {"question": "How to perform Cohort Analysis?", "answer": "Grouping users by shared characteristics to track behavior."},
            {"question": "What is Central Limit Theorem?", "answer": "Sampling distribution of mean is normal if sample size is large."},
            {"question": "Explain Simpson's Paradox.", "answer": "Trend appears in groups but reverses when combined."},
            {"question": "Handle outliers in analysis?", "answer": "Winsorization, Trimming, or non-parametric methods."},
            {"question": "What is a CTE?", "answer": "Temporary result set for reference in SQL statements."},
            {"question": "Explain Confidence Interval.", "answer": "Range likely to contain the population parameter."},
            {"question": "Dashboard design for executives?", "answer": "High-level KPIs, clear visuals, drill-down, actionable."},
            {"question": "What is Data Storytelling?", "answer": "Communicating insights using narratives and visuals."},
            {"question": "Leading vs. Lagging indicators?", "answer": "Leading predicts; Lagging confirms."}
        ],
        "Hard": [
            {"question": "How to calculate CLV?", "answer": "Avg Purchase Value * Frequency * Lifespan."},
            {"question": "Explain Causal Inference.", "answer": "Determining cause-and-effect relationships."},
            {"question": "How to detect Data Drift?", "answer": "Compare statistical properties over time."},
            {"question": "Explain Market Basket Analysis.", "answer": "Finding associations between products bought together."},
            {"question": "Z-test vs. T-test?", "answer": "Z-test for large samples; T-test for small samples."},
            {"question": "Optimize a slow SQL query?", "answer": "Index, avoid SELECT *, EXPLAIN, minimize subqueries."},
            {"question": "Explain Bayesian Statistics.", "answer": "Updating probabilities as more evidence is available."},
            {"question": "What is a Type II Error?", "answer": "False Negative (fail to reject false null)."},
            {"question": "Deal with Survivorship Bias?", "answer": "Include failed/dropped cases in the dataset."},
            {"question": "Explain Time Series Decomposition.", "answer": "Trend, Seasonality, and Residual components."}
        ]
    },
    "Data Engineer": {
        "Easy": [
            {"question": "What is ETL?", "answer": "Extract, Transform, Load - the process of moving data to a warehouse."},
            {"question": "Difference between SQL and NoSQL?", "answer": "SQL is relational/structured; NoSQL is non-relational/unstructured."},
            {"question": "What is a Data Warehouse?", "answer": "Central repository for integrated data from various sources."},
            {"question": "What is Spark?", "answer": "Unified analytics engine for large-scale data processing."},
            {"question": "Explain 'Data Integrity'.", "answer": "Accuracy, completeness, and consistency of data over its lifecycle."},
            {"question": "What is a Schema?", "answer": "The blueprint/structure of a database."},
            {"question": "Difference between OLAP and OLTP?", "answer": "OLAP for analysis/reporting; OLTP for transactions."},
            {"question": "What is HDFS?", "answer": "Hadoop Distributed File System for storing large files across clusters."},
            {"question": "What is a Data Lake?", "answer": "Storage for raw data in its native format until needed."},
            {"question": "What is JSON?", "answer": "JavaScript Object Notation - a lightweight data-interchange format."}
        ],
        "Medium": [
            {"question": "Explain 'Data Partitioning'.", "answer": "Dividing a database into distinct parts to improve performance."},
            {"question": "What is Apache Airflow?", "answer": "Platform to orchestrate complex computational workflows and pipelines."},
            {"question": "Difference between Batch and Stream processing?", "answer": "Batch processes data in blocks; Stream processes data in real-time."},
            {"question": "What is CAP Theorem?", "answer": "Consistency, Availability, Partition Tolerance - pick two in distributed systems."},
            {"question": "Explain 'Star Schema' vs 'Snowflake Schema'.", "answer": "Star consists of one fact table; Snowflake has normalized dimension tables."},
            {"question": "What is idempotency in data pipelines?", "answer": "The ability to run a job multiple times with the same result."},
            {"question": "How to handle slow-moving dimensions (SCD)?", "answer": "Type 1 (Overwrite), Type 2 (Add row), Type 3 (Add column)."},
            {"question": "What is a Message Queue?", "answer": "Asynchronous communication between services (e.g., Kafka, RabbitMQ)."},
            {"question": "Explain 'Data Lineage'.", "answer": "Tracking data origin and its transformations over time."},
            {"question": "What is Vertical vs Horizontal scaling?", "answer": "Vertical: more power to one machine; Horizontal: more machines."}
        ],
        "Hard": [
            {"question": "How does Spark's Catalyst Optimizer work?", "answer": "Optimizes queries through analysis, logical planning, and physical planning."},
            {"question": "Explain 'Consistency Models' in distributed databases.", "answer": "Strong, Eventual, and Causal consistency trade-offs."},
            {"question": "What is a 'Distributed Hash Table' (DHT)?", "answer": "Decentralized system providing lookup services similar to a hash table."},
            {"question": "Explain 'Write-Ahead Logging' (WAL).", "answer": "Technique for ensuring data integrity by logging changes before applying them."},
            {"question": "How to design a multi-tenant data architecture?", "answer": "Shared database vs. separate schemas vs. separate databases."},
            {"question": "Explain 'Vector Clocks'.", "answer": "Generating a partial ordering of events in a distributed system."},
            {"question": "What is 'Predicate Pushdown'?", "answer": "Filtering data at the source before loading into processing memory."},
            {"question": "How to handle 'Small File Problem' in HDFS?", "answer": "Sequence files, HAR files, or larger block sizes."},
            {"question": "Explain 'Log-Structured Merge-Tree' (LSM).", "answer": "Data structure used in many NoSQL databases for high-write loads."},
            {"question": "What is a 'Saga Pattern' in microservices?", "answer": "Managing transactions across multiple services using sequences of local transactions."}
        ]
    },
    "ML Engineer": {
        "Easy": [
            {"question": "What is a Neural Network?", "answer": "A computing system inspired by biological neural networks."},
            {"question": "Define 'Feature Engineering'.", "answer": "Selecting and transforming raw data into features that represent the underlying problem."},
            {"question": "What is an epoch?", "answer": "One full pass of the training dataset through the neural network."},
            {"question": "What is 'Target Leakage'?", "answer": "When information from the target variable 'leaks' into training features."},
            {"question": "Difference between classification and regression?", "answer": "Classification predicts labels; Regression predicts continuous values."},
            {"question": "What is an Activation Function?", "answer": "Defines the output of a node given an input or set of inputs."},
            {"question": "Explain 'Hyperparameters'.", "answer": "Parameters whose values are set before the learning process begins (e.g., learning rate)."},
            {"question": "What is Data Augmentation?", "answer": "Increasing the amount of data by adding slightly modified copies of existing data."},
            {"question": "What is a 'Dropout' in NN?", "answer": "Regularization technique that randomly ignores neurons during training."},
            {"question": "Difference between training and validation sets?", "answer": "Training is for learning; Validation is for tuning/selecting the best model."}
        ],
        "Medium": [
            {"question": "Explain 'Gradient Clipping'.", "answer": "Technique to prevent exploding gradients by limiting their maximum value."},
            {"question": "What is 'Transfer Learning'?", "answer": "Using a pre-trained model on a new, related task."},
            {"question": "Difference between Batch and Stochastic Gradient Descent?", "answer": "Batch uses full dataset; SGD uses one sample per update."},
            {"question": "Explain 'Early Stopping'.", "answer": "Ending training once performance on the validation set stops improving."},
            {"question": "What is 'Feature Scaling'?", "answer": "Normalizing or standardizing features to have a similar scale."},
            {"question": "Explain 'One-Hot Encoding'.", "answer": "Representing categorical variables as binary vectors."},
            {"question": "What is a 'Learning Rate Schedule'?", "answer": "Changing the learning rate during training (e.g., decay)."},
            {"question": "Difference between Generative and Discriminative models?", "answer": "Generative models P(x|y); Discriminative models P(y|x)."},
            {"question": "What is 'Gradient Boosting'?", "answer": "Building a strong model by sequentially adding learners that predict the residuals of the previous ones."},
            {"question": "Explain 'Word Embeddings'.", "answer": "Representing words as dense vectors in a continuous vector space (e.g., Word2Vec)."}
        ],
        "Hard": [
            {"question": "Explain 'Attention' and 'Self-Attention'.", "answer": "Mechanisms that allow models to weigh the importance of different parts of the input."},
            {"question": "What is a 'Transformer' architecture?", "answer": "Sequence-to-sequence model using self-attention, omitting recurrent/convolution layers."},
            {"question": "Explain 'Generative Adversarial Networks' (GANs).", "answer": "Generative model composed of a Generator and a Discriminator competing against each other."},
            {"question": "What is 'Model Quantization'?", "answer": "Reducing the precision of weights to decrease model size and speed up inference."},
            {"question": "Explain 'Differential Privacy' in ML.", "answer": "Framework to share information about a dataset while protecting individual privacy."},
            {"question": "What is 'Federated Learning'?", "answer": "Training models across decentralized servers or devices holding local data samples."},
            {"question": "Explain 'Explainability' vs 'Interpretability'.", "answer": "Interpretability is understanding why; Explainability is providing a post-hoc reason."},
            {"question": "What is 'Catastrophic Forgetting'?", "answer": "When a model loses previously learned information upon learning new data."},
            {"question": "Explain 'Binarized Neural Networks'.", "answer": "Neural networks with weights and activations constrained to -1 or +1."},
            {"question": "How do you deploy a model for low-latency inference?", "answer": "Model pruning, quantization, edge computing, or using specialized hardware (TPUs)."}
        ]
    }
}

def get_suggested_questions(role: str, difficulty: str, count: int = 20) -> list[dict]:
    """
    Fetch a randomized set of questions for a specific role and difficulty.
    """
    role_content = INTERVIEW_DB.get(role, INTERVIEW_DB["Data Scientist"])
    diff_content = role_content.get(difficulty, role_content["Medium"])
    
    # Shuffle and return slice
    pool = diff_content.copy()
    random.shuffle(pool)
    return pool[:count]
