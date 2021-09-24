import pytest
from asyncio import Future
from unittest.mock import Mock, AsyncMock
from src.bot.bot_commands import SignUpPhase, _start_sign_ups

phase = SignUpPhase()
channel_mock = Mock() 
message_mock = Mock() 
category_mock = Mock()
phase_mock = Mock()
ctx_mock = Mock()

@pytest.fixture(autouse=True)
def pytest_reset_mocks():
    channel_mock.reset_mock() 
    message_mock.reset_mock() 
    category_mock.reset_mock()
    phase_mock.reset_mock()
    ctx_mock.reset_mock()

@pytest.mark.asyncio
async def test_create_cateogory():
    category = 'category'
    future = Future()
    future.set_result(category)

    ctx_mock.guild.create_category.return_value = future 

    assert await phase._create_category(ctx_mock, category) == category
    ctx_mock.guild.create_category.assert_called_with(category)
    

@pytest.mark.asyncio
async def test_create_text_channel_category():
    channel, category = ['channel', 'category']
    future = Future()
    future.set_result(channel)

    ctx_mock.guild.create_text_channel.return_value = future

    assert await phase._create_text_channel_category(ctx_mock, channel, category) == channel
    ctx_mock.guild.create_text_channel.assert_called_with(name=channel, category=category)

@pytest.mark.asyncio
async def test_send_message_to_channel():
    reactions, message = ['reactions', 'message']
    channel_future = Future()
    message_future = Future()

    message_future.set_result(reactions)
    message_mock.add_reaction.return_value = message_future
    channel_future.set_result(message_mock)
    channel_mock.send.return_value = channel_future

    assert await phase._send_message_to_channel(message, channel_mock, reactions) == reactions

    message_mock.add_reaction.assert_called_with(reactions)
    channel_mock.send.assert_called_with(message)

@pytest.mark.asyncio
async def test_start_sign_ups():
    category, channel, reaction, message = ['category', 'channel', 'reaction', 'message']

    category_future = Future()
    channel_future = Future()
    reaction_future = Future()

    category_future.set_result(category)
    channel_future.set_result(channel)
    reaction_future.set_result(reaction)

    phase_mock._create_category.return_value = category_future
    phase_mock._create_text_channel_category.return_value = channel_future
    phase_mock._send_message_to_channel.return_value = reaction_future

    assert await _start_sign_ups(ctx_mock, category, channel, reaction, message, phase_mock) == { 
        'STATUS': 'start_up_completed',
        'category': category,
        'channel': channel,
        'reaction': reaction
    }

    phase_mock._create_category.assert_called_with(ctx_mock, category)
    phase_mock._create_text_channel_category.assert_called_with(ctx_mock, channel, category)
    phase_mock._send_message_to_channel.assert_called_with(message, channel, reaction)
