from old.generator.domain.state_machine import StateMachine


if __name__ == "__main__":
    sm = StateMachine()
    print(sm.get_next_state("page_view"))
