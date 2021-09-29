import pytest
from unittest.mock import Mock
from src.events.reaction import ReactionCoordinator
from src.tests.future_creator import future_creator

reaction_mock = Mock()
bot_mock = Mock()
tournament_state_mock = Mock()

@pytest.mark.asyncio
async def test_on_reaction_add():
    user_mock = 'test'
    bot_mock.user = 'test'
    reaction_coordinator = ReactionCoordinator(bot_mock, tournament_state_mock)
    result = await reaction_coordinator.on_reaction_add(reaction_mock, user_mock)
    assert result == None

    user_mock = Mock()
    reaction_mock.message.channel.category.name = 'tournament_test'
    tournament_state_mock.tournaments = { 'test': {'name': 'name'} }
    tournament_state_mock.player_signed_up.return_value = None
    user_mock.name = 'name'
    user_mock.send.return_value = future_creator(None)
    reaction_coordinator = ReactionCoordinator(bot_mock, tournament_state_mock)

    await reaction_coordinator.on_reaction_add(reaction_mock, user_mock)
    tournament_state_mock.player_signed_up.assert_called_with('test', 'name')

@pytest.mark.asyncio
async def on_raw_reaction_remove():
    user_mock = Mock()
    guild_mock = Mock()
    channel_mock  = Mock()
    category_mock = Mock()
    payload_mock = Mock()

    category_mock.name = 'test_test'
    channel_mock.category = category_mock
    guild_mock.get_channel.return_value = channel_mock
    user_mock.name = 'name'
    bot_mock.fetch_user.return_value = future_creator(user_mock)
    bot_mock.get_guild.return_value = guild_mock
    tournament_state_mock.tournaments = { 'test': {'name': 'name'} }
    tournament_state_mock.player_signed_up.return_value = None

    payload_mock.user_id = 'user_id'
    payload_mock.guild_id = 'guild_id'
    payload_mock.channel_id = 'channel_id'


    reaction_coordinator = ReactionCoordinator(bot_mock, tournament_state_mock)

    await reaction_coordinator.on_raw_reaction_remove()
    bot_mock.fetch_user.assert_called_with('user_id')
    bot_mock.get_guild.assert_called_with('guild_id')
    bot_mock.get_channel.assert_called_with('channel_id')
    tournament_state_mock.player_signed_up.assert_called_with('test', 'name')