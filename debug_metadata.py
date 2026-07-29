import utils.metadata

print(utils.metadata.__file__)

with open(utils.metadata.__file__, "r", encoding="utf-8") as f:
    print(f.read())