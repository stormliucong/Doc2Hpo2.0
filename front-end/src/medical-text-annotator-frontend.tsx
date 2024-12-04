import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Download, Trash2, Search } from 'lucide-react';

// Types for our application
interface Annotation {
  text: string;
  hpoTerm?: string;
  hpoId?: string;
  priority: 'normal' | 'high';
  start: number;
  end: number;
}

const MedicalTextAnnotator: React.FC = () => {
  // State variables
  const [inputText, setInputText] = useState<string>('');
  const [annotatedText, setAnnotatedText] = useState<string>('');
  const [annotations, setAnnotations] = useState<Annotation[]>([]);
  const [selectedAnnotation, setSelectedAnnotation] = useState<Annotation | null>(null);
  
  // Refs for text selection
  const textDisplayRef = useRef<HTMLDivElement>(null);

  // Handle text input submission
  const handleSubmit = async () => {
    try {
      // Call backend API to process text
      const response = await axios.post('http://localhost:5000/annotate', { text: inputText });
      
      // Update annotated text and annotations
      setAnnotatedText(response.data.annotated_text);
      setAnnotations(response.data.annotations);
    } catch (error) {
      console.error('Error submitting text:', error);
    }
  };

  // Handle text selection
  const handleTextSelection = () => {
    if (!textDisplayRef.current) return;

    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) return;

    const range = selection.getRangeAt(0);
    const selectedText = range.toString();

    if (selectedText.trim()) {
      // Open HPO term search modal
      openHPOSearchModal(selectedText, range);
    }
  };

  // Open HPO term search modal
  const openHPOSearchModal = async (text: string, range: Range) => {
    try {
      // Fetch HPO terms using the Clinical Tables API
      const response = await axios.get(`https://clinicaltables.nlm.nih.gov/api/hpo/v3/search?terms=${encodeURIComponent(text)}`);
      
      // TODO: Implement modal for HPO term selection
      const hpoTerm = response.data; // Process the response
      
      // Create new annotation
      const newAnnotation: Annotation = {
        text,
        hpoTerm: hpoTerm.name,
        hpoId: hpoTerm.id,
        priority: 'normal',
        start: range.startOffset,
        end: range.endOffset
      };

      setAnnotations([...annotations, newAnnotation]);
    } catch (error) {
      console.error('Error searching HPO terms:', error);
    }
  };

  // Delete annotation
  const deleteAnnotation = (index: number) => {
    const newAnnotations = [...annotations];
    newAnnotations.splice(index, 1);
    setAnnotations(newAnnotations);
  };

  // Change annotation priority
  const toggleAnnotationPriority = (index: number) => {
    const newAnnotations = [...annotations];
    newAnnotations[index].priority = 
      newAnnotations[index].priority === 'normal' ? 'high' : 'normal';
    setAnnotations(newAnnotations);
  };

  // Download annotations as CSV
  const downloadAnnotationsCSV = () => {
    const csvContent = [
      ['Text', 'HPO Term', 'HPO ID', 'Priority'],
      ...annotations.map(a => [
        a.text, 
        a.hpoTerm || '', 
        a.hpoId || '', 
        a.priority
      ])
    ].map(e => e.join(",")).join("\n");

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "medical_annotations.csv");
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Download annotated text as JSON
  const downloadAnnotatedJSON = () => {
    const jsonContent = JSON.stringify({
      original_text: inputText,
      annotated_text: annotatedText,
      annotations
    }, null, 2);

    const blob = new Blob([jsonContent], { type: 'application/json;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "medical_annotations.json");
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Generate gene predictions using Phen2Gene API
  const generateGenePredictions = async () => {
    try {
      const hpoTerms = annotations.map(a => a.hpoId).filter(Boolean);
      const response = await axios.post('https://phen2gene.wglab.org/api/pheno2gene', { hpo_terms: hpoTerms });
      // TODO: Handle gene prediction results
      console.log(response.data);
    } catch (error) {
      console.error('Error generating gene predictions:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Medical Text Annotator</CardTitle>
        </CardHeader>
        <CardContent>
          {/* Text Input Section */}
          <div className="mb-4">
            <Input 
              placeholder="Enter medical text here..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="mb-2"
            />
            <div className="flex space-x-2">
              <Button onClick={handleSubmit}>Annotate</Button>
              <Button 
                variant="secondary" 
                onClick={generateGenePredictions}
                disabled={annotations.length === 0}
              >
                Generate Gene Predictions
              </Button>
            </div>
          </div>

          {/* Annotated Text Display */}
          {annotatedText && (
            <div 
              ref={textDisplayRef}
              onMouseUp={handleTextSelection}
              className="mb-4 p-2 border rounded"
            >
              {/* TODO: Implement rich text display with highlights */}
              {annotatedText}
            </div>
          )}

          {/* Annotations Table */}
          {annotations.length > 0 && (
            <Card className="mb-4">
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle>Annotations</CardTitle>
                  <div className="flex space-x-2">
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={downloadAnnotationsCSV}
                    >
                      <Download className="mr-2 h-4 w-4" /> Download CSV
                    </Button>
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={downloadAnnotatedJSON}
                    >
                      <Download className="mr-2 h-4 w-4" /> Download JSON
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Text</TableHead>
                    <TableHead>HPO Term</TableHead>
                    <TableHead>Priority</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {annotations.map((annotation, index) => (
                    <TableRow key={index}>
                      <TableCell>{annotation.text}</TableCell>
                      <TableCell>{annotation.hpoTerm || 'N/A'}</TableCell>
                      <TableCell>
                        <Button 
                          variant={annotation.priority === 'high' ? 'destructive' : 'outline'}
                          size="sm"
                          onClick={() => toggleAnnotationPriority(index)}
                        >
                          {annotation.priority}
                        </Button>
                      </TableCell>
                      <TableCell>
                        <div className="flex space-x-2">
                          <Button 
                            size="sm" 
                            variant="outline"
                            onClick={() => {
                              // TODO: Implement HPO term search and update
                            }}
                          >
                            <Search className="h-4 w-4" />
                          </Button>
                          <Button 
                            size="sm" 
                            variant="destructive"
                            onClick={() => deleteAnnotation(index)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Card>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default MedicalTextAnnotator;
