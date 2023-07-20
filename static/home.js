document.addEventListener('DOMContentLoaded', () => {
  /**
   * @type {HTMLSelectElement}
   */
  const eleStorySelect = document.getElementById('story-select')
  const eleAnswerPrompt = document.getElementById('answer-prompt')

  eleAnswerPrompt.addEventListener('click', () => {
    if (eleStorySelect.value === '') return
    location.href = `/prompt/${eleStorySelect.value}`
  })
})