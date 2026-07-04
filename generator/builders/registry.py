# generator/builders/registry.py
from generator.builders.alpha_builder import AlphaBuilder
from generator.builders.beta_builder import BetaBuilder

BUILDERS = {
    "alpha": AlphaBuilder,
    "beta": BetaBuilder,
}
