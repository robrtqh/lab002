from unittest.mock import Mock

from lab3.event.game_event import GameEvent
from lab3.event.game_event_listener import GameEventListener
from lab3.event.game_event_publisher import GameEventPublisher
from lab3.event.game_event_type import GameEventType


def make_event(event_type: GameEventType) -> GameEvent:
    return GameEvent(event_type, hero=None, expedition=None)


def make_listener() -> Mock:
    return Mock(spec=GameEventListener)


def test_notifies_subscriber_of_matching_type():
    publisher = GameEventPublisher()
    listener = make_listener()
    publisher.subscribe(GameEventType.VICTORY, listener)
    event = make_event(GameEventType.VICTORY)

    publisher.publish(event)

    listener.on_event.assert_called_once_with(event)


def test_does_not_notify_subscriber_of_other_type():
    publisher = GameEventPublisher()
    listener = make_listener()
    publisher.subscribe(GameEventType.VICTORY, listener)

    publisher.publish(make_event(GameEventType.DEFEAT))

    listener.on_event.assert_not_called()


def test_notifies_all_subscribers_in_subscription_order():
    publisher = GameEventPublisher()
    calls = []
    first, second = make_listener(), make_listener()
    first.on_event.side_effect = lambda event: calls.append("первый")
    second.on_event.side_effect = lambda event: calls.append("второй")
    publisher.subscribe(GameEventType.VICTORY, first)
    publisher.subscribe(GameEventType.VICTORY, second)

    publisher.publish(make_event(GameEventType.VICTORY))

    assert calls == ["первый", "второй"]


def test_one_listener_can_subscribe_to_several_types():
    publisher = GameEventPublisher()
    listener = make_listener()
    publisher.subscribe(GameEventType.VICTORY, listener)
    publisher.subscribe(GameEventType.DEFEAT, listener)

    publisher.publish(make_event(GameEventType.VICTORY))
    publisher.publish(make_event(GameEventType.DEFEAT))

    assert listener.on_event.call_count == 2


def test_unsubscribed_listener_is_not_notified():
    publisher = GameEventPublisher()
    listener = make_listener()
    publisher.subscribe(GameEventType.VICTORY, listener)

    publisher.unsubscribe(GameEventType.VICTORY, listener)
    publisher.publish(make_event(GameEventType.VICTORY))

    listener.on_event.assert_not_called()


def test_publishing_without_subscribers_does_not_fail():
    GameEventPublisher().publish(make_event(GameEventType.LEVEL_UP))


def test_unsubscribing_unknown_listener_does_not_fail():
    GameEventPublisher().unsubscribe(GameEventType.VICTORY, make_listener())