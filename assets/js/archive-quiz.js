(() => {
  'use strict';
  const quiz = document.querySelector('[data-archive-quiz]');
  if (!quiz) return;
  const questions = [...quiz.querySelectorAll('.quiz-question')];
  const score = quiz.querySelector('#quiz-score');
  const reset = quiz.querySelector('#quiz-reset');
  function start() {
    score.textContent = '';
    reset.hidden = true;
    for (const question of questions) {
      delete question.dataset.result;
      question.querySelector('.quiz-evidence').hidden = true;
      question.querySelector('.quiz-outcome').textContent = '';
      question.querySelectorAll('button').forEach(button => {
        button.setAttribute('aria-pressed', 'false');
        button.removeAttribute('aria-disabled');
      });
    }
  }
  start();
  quiz.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (!button) return;
    if (button === reset) {
      start();
      questions[0]?.querySelector('button').focus();
      return;
    }
    const question = button.closest('.quiz-question');
    if (!question || question.dataset.result) return;
    const correct = button.dataset.correct === 'true';
    question.dataset.result = correct ? 'correct' : 'incorrect';
    question.querySelectorAll('button').forEach(answer => answer.setAttribute('aria-disabled', 'true'));
    button.setAttribute('aria-pressed', 'true');
    question.querySelector('.quiz-outcome').textContent = correct ? 'Correct.' : 'Not quite. The answer is below.';
    question.querySelector('.quiz-evidence').hidden = false;
    if (questions.every(item => item.dataset.result)) {
      const points = questions.filter(item => item.dataset.result === 'correct').length;
      score.textContent = `You got ${points} out of ${questions.length} correct.`;
      reset.hidden = false;
    }
  });
})();
