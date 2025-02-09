import React, { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "./Homepage.css";
import axios from "axios";
import { marked } from "marked";

const Homepage = ({ onUserInput }) => {
  const [typedTitle, setTypedTitle] = useState("");
  const [typedSubtext, setTypedSubtext] = useState("");
  const [inputText, setInputText] = useState("");
  const [isInputFocused, setIsInputFocused] = useState(true);
  const [stressLevel, setStressLevel] = useState(1);
  const [modelMessage, setModelMessage] = useState("");
  const [isBackgroundBlurred, setIsBackgroundBlurred] = useState(false);
  const [isVisualizerSlidDown, setIsVisualizerSlidDown] = useState(false);
  const [emotion, setEmotion] = useState("");
  const audioRef = useRef(null);
  const [currentAudio, setCurrentAudio] = useState("forest");
  const navigate = useNavigate();

  const fullTitle = "A.U.R.A";
  const subtext = "Analyze. Understand. Relax. Adapt.";

  useEffect(() => {
    let i = 0;
    let j = 0;
    setTypedTitle("");
    setTypedSubtext("");

    const titleInterval = setInterval(() => {
      if (i < fullTitle.length) {
        setTypedTitle((prev) => fullTitle.substring(0, i + 1));
        i++;
      } else {
        clearInterval(titleInterval);

        // Start typing the subtext after the title is complete
        const subtextInterval = setInterval(() => {
          if (j < subtext.length) {
            setTypedSubtext((prev) => subtext.substring(0, j + 1));
            j++;
          } else {
            clearInterval(subtextInterval);
          }
        }, 100);
      }
    }, 150);

    return () => {
      clearInterval(titleInterval);
    };
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

  const handleSendInput = async () => {
    if (inputText.trim()) {
      setIsInputFocused(false);
      setIsBackgroundBlurred(true);
      setIsVisualizerSlidDown(true);

      try {
        const API_BASE_URL = import.meta.env.VITE_BACKEND_URL;

        const response = await axios.post(`${API_BASE_URL}/api/analyze`,{
          input_text: inputText,
        });

        const { sentiment, sentiment_score, emotions, tips } = response.data;
        const primaryEmotion = Object.keys(emotions)[0];
        const primaryEmotionValue = emotions[primaryEmotion];
        const simulatedStressLevel = Math.floor(sentiment_score * 100);

        console.log(
          `First Emotion: ${primaryEmotion}, Value: ${primaryEmotionValue}`
        );

        setModelMessage(tips);
        setEmotion(primaryEmotion);
        setInputText("");

        animateStressLevel(simulatedStressLevel);
      } catch (error) {
        console.error("Error analyzing input:", error);
      }
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
    }, 10);
  };

  const barCount = Math.ceil(window.innerWidth / 6);

  useEffect(() => {
    if (emotion) {
      const pulsatingLight = document.querySelector(".pulsatingLight");
      const spreadingLight = document.querySelector(".spreadingLight");
      if (pulsatingLight && spreadingLight) {
        pulsatingLight.className = `pulsatingLight ${emotion.toLowerCase()}`;
        spreadingLight.className = `spreadingLight ${emotion.toLowerCase()}`;
      }
    }
  }, [emotion]);

  return (
    <div className="container">
      <div className="loader"></div>

      {/* Title Section */}
      <div className="titleContainer">
        <div className="title">{typedTitle}</div>
        <div className="subtext">
          {typedSubtext}
          <span className={typedSubtext.length < subtext.length ? "cursor" : ""}></span>
        </div>
      </div>

      {/* Visualizer Container */}
      <div
        className={`visualizerContainer ${
          isVisualizerSlidDown ? "slideDown" : ""
        }`}
      >
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

      {/* Pulsating Light */}
      {emotion && (
        <motion.div
          className={`pulsatingLight ${emotion.toLowerCase()}`}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.6, 1, 0.6],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
          }}
        />
      )}
      {emotion && (
        <motion.div
          className={`spreadingLight ${emotion.toLowerCase()}`}
          animate={{
            scale: [1, 1.5, 1],
            opacity: [0.4, 0.8, 0.4],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
          }}
        />
      )}

      {/* Input Container */}
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
            <div className="meterArc"></div>
            <div
              className="meterIndicator"
              style={{
                transform: `rotate(${(stressLevel / 100) * 180 - 90}deg)`,
              }}
            />
            <div className="stressLevel">{stressLevel}</div>
          </div>

          <div className="modelMessage">
            <Typewriter text={modelMessage} />
          </div>
        </div>
      )}

      <audio
        ref={audioRef}
        src={`/public/audio/${currentAudio}.flac`}
        autoPlay
        loop
      />

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

  return <div dangerouslySetInnerHTML={{ __html: marked(displayedText.replace(/\n/g, "<br />")) }} />;
};

export default Homepage;
