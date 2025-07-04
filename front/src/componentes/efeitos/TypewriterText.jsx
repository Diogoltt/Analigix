import React, { useState, useEffect } from 'react';

const TypewriterText = ({ text, speed = 50, onComplete }) => {
    const [displayText, setDisplayText] = useState('');
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        if (currentIndex < text.length) {
            const timeout = setTimeout(() => {
                setDisplayText(prev => prev + text[currentIndex]);
                setCurrentIndex(prev => prev + 1);
            }, speed);

            return () => clearTimeout(timeout);
        } else if (currentIndex === text.length && onComplete) {
            onComplete();
        }
    }, [currentIndex, text, speed, onComplete]);

    useEffect(() => {
        setDisplayText('');
        setCurrentIndex(0);
    }, [text]);

    return (
        <span>
            {displayText}
            {currentIndex < text.length && (
                <span className="typewriter-cursor">|</span>
            )}
        </span>
    );
};

export default TypewriterText;
