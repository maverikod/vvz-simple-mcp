from setuptools import setup


setup(
    name="simple-mcp",
    version="0.1.0",
    description="FastMCP Echo OAuth Server",
    py_modules=["server"],
    install_requires=[
        "fastmcp",
        "fastapi",
        "uvicorn",
        "requests",
        "python-dotenv",
    ],
    python_requires=">=3.10",
)
