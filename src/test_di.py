from containers import Container

container = Container()
container.wire(modules=["apis.users.controller.user_controller"])

user_service = container.user_service()

async def hi():
    print(await user_service.test())
    print('HELLO')

hi()

