import React, { useState } from 'react';
import './PracticeQuestion.css';

// ダミーデータ
const dummyQuestion = {
  id: 'q1',
  category: '一般問題',
  year: 2023,
  questionNumber: 1,
  questionText: '図のような単相2線式回路で、抵抗負荷の両端の電圧Vが100V、消費電力が0.5kWであるとき、電線1線あたりの抵抗r[Ω]はいくらか。',
  questionImage: 'https://via.placeholder.com/400x200.png?text=Question+Image',
  choices: [
    { id: 'c1', text: '0.1' },
    { id: 'c2', text: '0.2' },
    { id: 'c3', text: '0.3' },
    { id: 'c4', text: '0.4' },
  ],
  answer: 'c2',
  explanation: '解説テキストがここに入ります。'
};


const PracticeQuestion = () => {
  const [selectedChoice, setSelectedChoice] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);

  const handleChoiceClick = (choiceId: string) => {
    setSelectedChoice(choiceId);
    setIsCorrect(choiceId === dummyQuestion.answer);
  };

  return (
    <div className="question-container">
      <div className="question-header">
        <span className="category">{dummyQuestion.category}</span>
        <span className="year-number">令和{dummyQuestion.year - 2018}年 - 問{dummyQuestion.questionNumber}</span>
      </div>
      <p className="question-text">{dummyQuestion.questionText}</p>
      {dummyQuestion.questionImage && (
        <img src={dummyQuestion.questionImage} alt="問題図" className="question-image" />
      )}
      <div className="choices-grid">
        {dummyQuestion.choices.map((choice) => (
          <button
            key={choice.id}
            className={`choice-button ${selectedChoice === choice.id ? (isCorrect ? 'correct' : 'incorrect') : ''}`}
            onClick={() => handleChoiceClick(choice.id)}
            disabled={selectedChoice !== null}
          >
            {choice.text}
          </button>
        ))}
      </div>
      {selectedChoice && (
        <div className={`result-display ${isCorrect ? 'correct-text' : 'incorrect-text'}`}>
          {isCorrect ? '正解！' : '不正解...'}
          <p className="explanation">{dummyQuestion.explanation}</p>
        </div>
      )}
    </div>
  );
};

export default PracticeQuestion;

