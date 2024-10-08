from decimal import Decimal
import re


SOLANA_LAMPORTS = 1000000000.0
SOLANA_REGEX= "[1-9A-HJ-NP-Za-km-z]{32,44}"


def convert_to_solana(value: int) -> str:
    value = int(value)
    res = Decimal(value) / Decimal(SOLANA_LAMPORTS)
    return str(res)


def convert_to_tokens(value: int, decimals: int) -> str:
    value = int(value)
    res = Decimal(value) / Decimal(10 ** decimals)
    return str(res)


def format_solana_addresses(text: str) -> str:

    def replace(match):
        return f'<a href="https://explorer.solana.com/address/{match.group()}">{match.group().strip()}</a>'

    result = re.sub(SOLANA_REGEX, replace, text)

    return result
