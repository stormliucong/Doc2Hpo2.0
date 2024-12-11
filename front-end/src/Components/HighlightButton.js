import React, { useState, useRef } from "react";
import { Button } from "@mui/material";
import Chip from "@mui/material/Chip";
import Tooltip from "@mui/material/Tooltip";
import { styled } from "@mui/material/styles";
import { tooltipClasses } from "@mui/material/Tooltip";
import { Typography } from "@mui/material";


const HighlightButton = ({ highlight, highlightedText, onUpdateHighlight, onDeleteHighlight, onClickHighlight }) => {
    const [clickCount, setClickCount] = useState(0);
    const timerRef = useRef(null);
    const longPressTimeoutRef = useRef(null);
    const highlightColors = ["#FFC107", "#FF5722"]; // Modern color palette
    const longPressDelay = 1000; // Time in ms to detect long press

    const HtmlTooltip = styled(({ className, ...props }) => (
        <Tooltip {...props} classes={{ popper: className }} />
      ))(({ theme }) => ({
        [`& .${tooltipClasses.tooltip}`]: {
          backgroundColor: '#f5f5f9',
          color: 'rgba(0, 0, 0, 0.87)',
          maxWidth: 220,
          fontSize: theme.typography.pxToRem(12),
          border: '1px solid #dadde9',
        },
      }));

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
        onClickHighlight(highlight);
    };

    const onDoubleClick = () => {
        onDeleteHighlight(highlight);
    };

    const onSingleClick = () => {
        onUpdateHighlight({ ...highlight, priority: highlight.priority === 'Normal' ? 'High' : 'Normal' });

    };
    
    return (
        <HtmlTooltip
        title={
          <React.Fragment>
            
            {highlight.hpoAttributes.id && (
                <>
                <b>{highlight.hpoAttributes.name}</b> <br />
                <em>{highlight.hpoAttributes.id}</em>  
                </>
            )}

            {!highlight.hpoAttributes.id && (
                <>
                 <b>No HPO ID found</b> <br />
                 <em>Long press to search.</em>
                </>
            )}
          </React.Fragment>
        }
      >
        <Button
            onMouseDown={handleMouseDown}
            onMouseUp={handleMouseUp}
            onClick={handleClick}
            style={{
                color: highlight.priority === 'Normal' ? highlightColors[0] : highlightColors[1],
                padding: "auto",
                margin: "auto",
                fontSize: "inherit",
                textTransform: "none",
                cursor: "pointer",
                display: 'inline-block', // Ensures button stays inline
            }}
            variant="text"
            size="small"
        >
            {highlightedText}
            
        </Button>
        </HtmlTooltip>
    );
};

export default HighlightButton;
