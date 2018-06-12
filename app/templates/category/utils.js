export function removeFlashMessages() {
  const list = $('.flash-message__list')

  const intervalId = setInterval(() => {
    setTimeout(function() {
      if (list.length == 0) {
        clearInterval(intervalId)
      } else {
        const message = list.find('>:first-child')
        message.slideUp('300', function() {
          this.parentNode.removeChild(this)
        })
      }

    }, 2000)

  }, 2000)
}
