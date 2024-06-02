let messages = {{messages}};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fill_playground(messages) {
  let system_messages = messages.filter(msg => msg.role === 'system');
  if (system_messages.length > 0) {
    let system_message_textarea = document.querySelector('.chat-pg-instructions textarea');
    if (system_message_textarea) {
      system_message_textarea.focus();
      system_message_textarea.value = '';
      if (document.execCommand) {
        document.execCommand("insertText", false, system_messages[0].content);
      }
      await new Promise(requestAnimationFrame);
    }
  }

  let remove_buttons = document.querySelectorAll('.chat-message-remove-button');
  if (remove_buttons) {
    for (let button of remove_buttons) {
      let clickEvent = new MouseEvent('click', {
        bubbles: true,
        cancelable: true
      });
      button.dispatchEvent(clickEvent);
    }
  }

  let other_messages = messages.filter(msg => msg.role !== 'system');
  for (let message of other_messages) {
    document.querySelector('.add-message').click();
    await new Promise(requestAnimationFrame);
  }

  for (let i = 0; i < other_messages.length; i++) {
    let all_elements = document.querySelectorAll('.text-input-with-focus');
    if (all_elements.length > i) {
      let textarea_to_fill = all_elements[i].querySelector('textarea');
      if (textarea_to_fill) {
        textarea_to_fill.focus();
        if (document.execCommand) {
          document.execCommand("insertText", false, other_messages[i].content);
        }
        await new Promise(requestAnimationFrame);
      }
    }
  }
}

fill_playground(messages);
