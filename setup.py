from setuptools import setup

setup(
    name='zoom_autojoiner_gui',
    packages=['zoom_autojoiner_gui'],
    include_package_data=True,
    install_requires=[
		'sqlalchemy',
		'pyautogui',
                'pillow',
    ],
)
