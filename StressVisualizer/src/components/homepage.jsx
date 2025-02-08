import React, { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "./Homepage.css";

const Homepage = ({ onUserInput }) => {
  const [typedTitle, setTypedTitle] = useState("");
  const [inputText, setInputText] = useState("");
  const [isInputFocused, setIsInputFocused] = useState(true); // Input always visible until submitted
  const [stressLevel, setStressLevel] = useState(1); // Start from 1
  const [modelMessage, setModelMessage] = useState("");
  const [isBackgroundBlurred, setIsBackgroundBlurred] = useState(false);
  const [isVisualizerSlidDown, setIsVisualizerSlidDown] = useState(false); // State for sliding effect
  const [emotion, setEmotion] = useState(""); // State for the emotion (happy, angry, etc.)
  const audioRef = useRef(null);
  const [currentAudio, setCurrentAudio] = useState("forest");
  const navigate = useNavigate();

  const fullTitle = "STRESS VISUALIZER";

  useEffect(() => {
    let i = 0;
    setTypedTitle("");
    const interval = setInterval(() => {
      if (i < fullTitle.length) {
        setTypedTitle((prev) => fullTitle.substring(0, i + 1));
        i++;
      } else {
        clearInterval(interval);
      }
    }, 150);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.play();
    }
  }, [currentAudio]);

  const handleToggleSwitch = () => {
    const newAudio = currentAudio === "forest" ? "water" : "forest";
    setCurrentAudio(newAudio);
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.src = `/public/audio/${newAudio}.flac`;
      audioRef.current.play();
    }
  };

  const handleSendInput = () => {
    if (inputText.trim()) {
      setIsInputFocused(false); // Move input to the top
      setIsBackgroundBlurred(true); // Apply blur effect

      // Trigger the visualizer slide-down effect
      setIsVisualizerSlidDown(true);

      const simulatedStressLevel = Math.floor(Math.random() * 100) + 1;
      const simulatedMessage = generateModelMessage(simulatedStressLevel);

      setModelMessage(simulatedMessage);
      setEmotion(determineEmotion(simulatedStressLevel)); // Set the emotion based on stress level
      setInputText("");

      // Animate the stress level from 1 to simulatedStressLevel
      animateStressLevel(simulatedStressLevel);
    }
  };

  const animateStressLevel = (targetLevel) => {
    let currentLevel = stressLevel;
    const interval = setInterval(() => {
      if (currentLevel < targetLevel) {
        currentLevel++;
        setStressLevel(currentLevel);
      } else {
        clearInterval(interval);
      }
    }, 10); // Update every 10ms
  };

  const generateModelMessage = (stress) => {
    if (stress < 20) return "You're feeling relaxed. Keep it up!";
    if (stress < 50) return "You seem slightly stressed, try to relax.";
    if (stress < 75) return "You're quite stressed. Take some time to breathe!";
    return "You're highly stressed. Consider taking a break or meditating.";
  };

  const determineEmotion = (stress) => {
    if (stress < 20) return "happy"; // Happy for low stress
    if (stress >= 20 && stress < 40) return "anxiety"; // Anxiety for medium-low stress
    if (stress >= 40 && stress < 60) return "sad"; // Sad for medium stress
    if (stress >= 60 && stress < 80) return "fear"; // Fear for higher stress
    return "angry"; // Angry for high stress
  };

  const barCount = Math.ceil(window.innerWidth / 6);

  return (
    <div className="container">
      <div className="loader"></div>

      <div className="title">
        {typedTitle}
        <span className={typedTitle.length < fullTitle.length ? "cursor" : ""}></span>
      </div>

      {/* Visualizer Container with slideDown class */}
      <div className={`visualizerContainer ${isVisualizerSlidDown ? "slideDown" : ""}`}>
        {Array.from({ length: barCount }).map((_, index) => (
          <motion.div
            key={index}
            className="bar"
            style={{ height: `${Math.random() * 60 + 20}px` }}
            animate={{
              scaleY: [1, 1.5, 1],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              repeatType: "mirror",
              delay: index * 0.05,
            }}
          />
        ))}
      </div>

      {/* Pulsating Light based on Emotion */}
      {emotion && (
        <>
          <div className={`pulsatingLight ${emotion}`} />
          <div className={`spreadingLight ${emotion}`} />
        </>
      )}

      {isInputFocused && (
        <div className="inputContainer">
          <input
            className="textInput"
            type="text"
            placeholder="Type something to relax..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSendInput()}
          />
          <button className="sendButton" onClick={handleSendInput}>
            ➤
          </button>
        </div>
      )}

      {/* Response Container */}
      {!isInputFocused && (
        <div className="responseContainer">
          <div className="stressMeter">
            {/* Arc background */}
            <div className="meterArc"></div>

            {/* Meter Needle */}
            <div
              className="meterIndicator"
              style={{
                transform: `rotate(${(stressLevel / 100) * 180 - 90}deg)`, // Rotate based on stress level
              }}
            />

            {/* Stress Level */}
            <div className="stressLevel">{stressLevel}</div>
          </div>

          <div className="modelMessage">
            <Typewriter text={modelMessage} />
          </div>
        </div>
      )}

      <audio ref={audioRef} src={`/public/audio/${currentAudio}.flac`} autoPlay loop />

      <div className="switch">
        <label>
          <input type="checkbox" onChange={handleToggleSwitch} />
          <span className="slider"></span>
        </label>
      </div>
    </div>
  );
};

const Typewriter = ({ text }) => {
  const [displayedText, setDisplayedText] = useState("");
  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      if (i < text.length) {
        setDisplayedText((prev) => prev + text.charAt(i));
        i++;
      } else {
        clearInterval(interval);
      }
    }, 100);
    return () => clearInterval(interval);
  }, [text]);

  return <div>{displayedText}</div>;
};

export default Homepage;
