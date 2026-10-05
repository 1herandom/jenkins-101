import fire

def hello(name="World"):
    while True:
        print("Hello %s!" % name)

if __name__ == '__main__':
    fire.Fire(hello)
