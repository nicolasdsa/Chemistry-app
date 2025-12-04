from models.instrument import Instrument


def split_instruments_by_container(instruments: list[Instrument]) -> tuple[list[Instrument], list[Instrument]]:
    transfer_instruments = [inst for inst in instruments if not inst.is_container]
    container_instruments = [inst for inst in instruments if inst.is_container]
    return transfer_instruments, container_instruments
