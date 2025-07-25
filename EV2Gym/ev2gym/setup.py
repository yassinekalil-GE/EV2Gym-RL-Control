from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Core requirements (without optional dependencies)
core_requirements = [
    "gymnasium>=0.29.0",
    "numpy>=1.21.0", 
    "pandas>=1.3.0",
    "matplotlib>=3.5.0",
    "pyyaml>=6.0",
    "scipy>=1.7.0",
    "tqdm>=4.64.0",
    "seaborn>=0.11.0"
]

setup(
    name="ev2gym",
    version="1.0.0",
    author="EV2Gym Team",
    description="A comprehensive electric vehicle charging simulation environment for smart grid research",
    long_description="""
    EV2Gym is a Gymnasium-based simulation environment for electric vehicle (EV) charging research.
    It provides realistic modeling of EV charging behavior, grid constraints, and Vehicle-to-Grid (V2G) 
    capabilities. The environment supports reinforcement learning, optimization baselines, and 
    standalone simulations for smart charging algorithm development.
    
    Key Features:
    - Realistic EV charging simulation with V2G support
    - Multiple charging scenarios (public, private, workplace)
    - Grid constraints and transformer modeling
    - Real-world data integration (Netherlands electricity market)
    - RL-ready Gymnasium environment
    - Optimization baselines and heuristics
    - Comprehensive visualization tools
    """,
    long_description_content_type="text/plain",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
    install_requires=core_requirements,
    extras_require={
        "optimization": ["gurobipy>=10.0.0"],
        "ml": ["torch>=1.12.0", "stable-baselines3>=2.0.0"],
        "web": ["streamlit>=1.25.0", "dash>=2.10.0", "plotly>=5.0.0"],
        "jupyter": ["jupyter>=1.0.0", "ipywidgets>=7.6.0"],
        "dev": ["pytest>=7.0.0", "pytest-cov>=4.0.0"],
        "all": [
            "gurobipy>=10.0.0", "torch>=1.12.0", "stable-baselines3>=2.0.0",
            "streamlit>=1.25.0", "dash>=2.10.0", "plotly>=5.0.0",
            "jupyter>=1.0.0", "ipywidgets>=7.6.0", "pytest>=7.0.0", "pytest-cov>=4.0.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "ev2gym-demo=ev2gym.tools.demo:main",
            "ev2gym-cli=ev2gym.tools.cli:main",
            "ev2gym-web=ev2gym.tools.web_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ev2gym": [
            "data/*.csv",
            "data/*.json", 
            "data/*.npy",
            "example_config_files/*.yaml",
            "example_config_files/*.json",
            "visuals/icons/*"
        ],
    },
)
