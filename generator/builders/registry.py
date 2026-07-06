# generator/builders/registry.py
from generator.builders.alpha_builder import AlphaBuilder
from generator.builders.beta_builder import BetaBuilder
from generator.builders.gamma_builder import GammaBuilder

BUILDERS = {
    "alpha": AlphaBuilder,
    "beta": BetaBuilder,
    "gamma": GammaBuilder,
}
