import React, { useState, useRef } from "react";
import { Button } from "@mui/material";

const HighlightButton = ({ highlight, highlightedText, onUpdateHighlight, onDeleteHighlight, onClickHighlight }) => {
    const [clickCount, setClickCount] = useState(0);
    const timerRef = useRef(null);
    const longPressTimeoutRef = useRef(null);
    const highlightColors = ["#FFC107", "#FF5722"]; // Modern color palette
    const longPressDelay = 1000; // Time in ms to detect long press

    const handleMouseDown = () => {
        longPressTimeoutRef.current = setTimeout(() => {
            onLongPress && onLongPress();
            setClickCount(0); // Reset to avoid firing single/double click after long press
        }, longPressDelay);
    };

    const handleMouseUp = () => {
        clearTimeout(longPressTimeoutRef.current); // Prevent long press if the button is released early
    };

    const handleClick = () => {
        clearTimeout(timerRef.current);

        setClickCount((prev) => {
            const newCount = prev + 1;

            if (newCount === 1) {
                timerRef.current = setTimeout(() => {
                    if (newCount === 1) {
                        onSingleClick && onSingleClick();
                    }
                    setClickCount(0); // Reset count after single click
                }, 300); // Timeout for distinguishing single and double click
            } else if (newCount === 2) {
                onDoubleClick && onDoubleClick();
                setClickCount(0); // Reset count after double click
            }

            return newCount;
        });
    };

    const onLongPress = () => {
        // Pass the updated highlight back to the parent
        onUpdateHighlight({ ...highlight, priority: highlight.priority === 'Normal' ? 'High' : 'Normal' });
    };

    const onDoubleClick = () => {
        onDeleteHighlight(highlight);
    };

    const onSingleClick = () => {
        onClickHighlight(highlight);
    };
    
    return (
        <Button
            onMouseDown={handleMouseDown}
            onMouseUp={handleMouseUp}
            onClick={handleClick}
            style={{
                backgroundColor: highlight.priority === 'Normal' ? highlightColors[0] : highlightColors[1],
                color: "#FFFFFF",
                padding: "0 5px",
                margin: "0 2px",
                borderRadius: "4px",
                fontSize: "inherit",
                textTransform: "none",
                cursor: "pointer",
            }}
            variant="contained"
            size="small"
        >
            {highlightedText}
        </Button>
    );
};

export default HighlightButton;
