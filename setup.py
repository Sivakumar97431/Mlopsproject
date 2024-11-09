from setuptools import find_packages,setup
from typing import List



def requirements()->List[str]:
    requirement_List: List[str]=[]
    try:
        with open("requirements.txt","r") as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!="-e .":
                    requirement_List.append(requirement)
    except Exception as e:
        print("Requirements.txt file not found")
    return requirement_List
print(requirements())

setup(
    name="Network Security",
    version="0.0.1",
    author="siva kumar",
    author_email="mshivakumarreddy78@gmail.com",
    packages=find_packages(),
    install_requires=requirements()
)
        