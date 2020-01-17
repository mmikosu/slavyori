owners = [
    254036166108512257      # Mikosu
]

version = "v1.0.0"
invite = "https://discord.gg/UhYGRkq"


def is_owner(ctx):
    return ctx.author.id in owners
