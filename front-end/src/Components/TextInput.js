import React from "react";

const TextInput = ({ label, value, setValue }) => {
    const [inputText, setInputText] = useState("");

    return (
        <>
        <TextField
          fullWidth
          label="Input Text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />

        <Button variant="contained" onClick={handleTextSubmit} sx={{ mt: 1 }}>
          Submit
        </Button>
        </>
    );
}