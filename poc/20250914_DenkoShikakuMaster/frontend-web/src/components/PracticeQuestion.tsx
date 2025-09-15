import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PracticeQuestion.css';

// データ構造の型定義
interface Choice {
  id: string;
  text: string;
}

interface Question {
  id: string;
  category: string;
  year: number;
  questionNumber: number;
  questionText: string;
  questionImage?: string;
  choices: Choice[];
  answer: string;
  explanation: string;
}

const PracticeQuestion = () => {
  const [question, setQuestion] = useState<Question | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  const [selectedChoice, setSelectedChoice] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);

  useEffect(() => {
    // バックエンドからデータを取得
    axios.get('http://localhost:3010/questions')
      .then(response => {
        setQuestion(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching question:", err);
        setError('問題の読み込みに失敗しました。');
        setLoading(false);
      });
  }, []); // 空の配列を渡すことで、コンポーネントのマウント時に一度だけ実行される

  const handleChoiceClick = (choiceId: string) => {
    if (!question) return;
    setSelectedChoice(choiceId);
    setIsCorrect(choiceId === question.answer);
  };
  
  if (loading) {
    return <div className="loading-message">問題データを読み込み中...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!question) {
    return <div className="error-message">問題データがありません。</div>;
  }

  return (
    <div className="question-container">
      <div className="question-header">
        <span className="category">{question.category}</span>
        <span className="year-number">令和{question.year - 2018}年 - 問{question.questionNumber}</span>
      </div>
      <p className="question-text">{question.questionText}</p>
      {question.questionImage && (
        <img src={question.questionImage} alt="問題図" className="question-image" />
      )}
      <div className="choices-grid">
        {question.choices.map((choice) => (
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
          <p className="explanation">{question.explanation}</p>
        </div>
      )}
    </div>
  );
};

export default PracticeQuestion;
