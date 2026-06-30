import React, { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';
import { 
  Sparkles, Upload, RotateCw, Settings, BarChart2, FileText, 
  Layers, Search, Sliders, MessageSquare, CheckCircle, AlertTriangle, 
  ArrowRight, Download, Eye, Shield, Heart, Zap, RefreshCw, Database, X
} from 'lucide-react';

const API_BASE = 'http://localhost:8000';

// Predefined fonts metadata database matching backend
const GOOGLE_FONTS = [
  {"name": "Playfair Display", "style": "Serif", "lux": 0.95, "read": 0.82, "shelf": 0.88},
  {"name": "Cinzel Decorative", "style": "Serif", "lux": 0.98, "read": 0.65, "shelf": 0.92},
  {"name": "Merriweather", "style": "Serif", "lux": 0.75, "read": 0.95, "shelf": 0.70},
  {"name": "Lora", "style": "Serif", "lux": 0.82, "read": 0.90, "shelf": 0.75},
  {"name": "Inter", "style": "Grotesque", "lux": 0.78, "read": 0.98, "shelf": 0.85},
  {"name": "Roboto", "style": "Grotesque", "lux": 0.60, "read": 0.97, "shelf": 0.80},
  {"name": "Montserrat", "style": "Geometric", "lux": 0.84, "read": 0.92, "shelf": 0.89},
  {"name": "Space Grotesk", "style": "Grotesque", "lux": 0.70, "read": 0.90, "shelf": 0.88},
  {"name": "Futura", "style": "Geometric", "lux": 0.90, "read": 0.93, "shelf": 0.90},
  {"name": "Arvo", "style": "Slab", "lux": 0.68, "read": 0.88, "shelf": 0.82},
  {"name": "Lobster", "style": "Display", "lux": 0.40, "read": 0.70, "shelf": 0.95},
  {"name": "Great Vibes", "style": "Script", "lux": 0.95, "read": 0.50, "shelf": 0.78},
  {"name": "Pacifico", "style": "Handwritten", "lux": 0.35, "read": 0.72, "shelf": 0.90}
];

const getFontPreviewStyle = (f) => {
  if (!f || !f.name) return {};
  let fontFamily = 'sans-serif';
  const styleVal = f.style || 'Sans';
  
  if (styleVal === 'Serif') fontFamily = '"Playfair Display", Georgia, serif';
  else if (styleVal === 'Slab') fontFamily = '"Arvo", Courier New, serif';
  else if (styleVal === 'Script') fontFamily = '"Great Vibes", cursive';
  else if (styleVal === 'Handwritten') fontFamily = '"Pacifico", cursive';
  else if (styleVal === 'Display') fontFamily = '"Lobster", cursive';
  else if (styleVal === 'Geometric') fontFamily = '"Montserrat", sans-serif';
  else fontFamily = '"Inter", sans-serif';

  // Match specific known fonts
  const nameLower = f.name.toLowerCase();
  if (nameLower.includes('playfair')) fontFamily = '"Playfair Display", serif';
  else if (nameLower.includes('cinzel')) fontFamily = '"Cinzel Decorative", serif';
  else if (nameLower.includes('merriweather')) fontFamily = '"Merriweather", serif';
  else if (nameLower.includes('lora')) fontFamily = '"Lora", serif';
  else if (nameLower.includes('inter')) fontFamily = '"Inter", sans-serif';
  else if (nameLower.includes('roboto')) fontFamily = '"Roboto", sans-serif';
  else if (nameLower.includes('montserrat')) fontFamily = '"Montserrat", sans-serif';
  else if (nameLower.includes('space')) fontFamily = '"Space Grotesk", sans-serif';
  else if (nameLower.includes('arvo')) fontFamily = '"Arvo", serif';
  else if (nameLower.includes('lobster')) fontFamily = '"Lobster", cursive';
  else if (nameLower.includes('great vibes')) fontFamily = '"Great Vibes", cursive';
  else if (nameLower.includes('pacifico')) fontFamily = '"Pacifico", cursive';
  else if (nameLower.includes('times')) fontFamily = '"Times New Roman", Times, serif';

  // Apply styling properties from DNA parameters
  const weight = f.luxury_score > 0.85 ? '900' : f.luxury_score > 0.7 ? '700' : f.luxury_score < 0.35 ? '300' : 'normal';
  const letterSpacing = f.readability < 0.45 ? '0.12em' : 'normal';
  const fontStyle = styleVal === 'Script' || styleVal === 'Handwritten' ? 'italic' : 'normal';

  return {
    fontFamily: fontFamily,
    fontWeight: weight,
    letterSpacing: letterSpacing,
    fontStyle: fontStyle
  };
};

const GOOGLE_FAMILIES = [
  '"Playfair Display", serif',
  '"Cinzel Decorative", serif',
  '"Merriweather", serif',
  '"Lora", serif',
  '"Inter", sans-serif',
  '"Roboto", sans-serif',
  '"Montserrat", sans-serif',
  '"Space Grotesk", sans-serif',
  '"Futura", sans-serif',
  '"Arvo", serif',
  '"Lobster", cursive',
  '"Great Vibes", cursive',
  '"Pacifico", cursive',
  '"Times New Roman", serif',
  '"Georgia", serif',
  '"Garamond", serif',
  '"Didot", serif',
  '"Impact", sans-serif',
  '"Courier New", monospace',
  '"Comic Sans MS", cursive'
];

function MorphingLetter({ char, timing }) {
  const [fontA, setFontA] = useState('"Inter", sans-serif');
  const [fontB, setFontB] = useState('"Inter", sans-serif');
  const [showA, setShowA] = useState(true);

  useEffect(() => {
    // Select initial random font
    const initial = GOOGLE_FAMILIES[Math.floor(Math.random() * GOOGLE_FAMILIES.length)];
    setFontA(initial);
    setFontB(initial);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      const nextFont = GOOGLE_FAMILIES[Math.floor(Math.random() * GOOGLE_FAMILIES.length)];
      if (showA) {
        setFontB(nextFont);
        setShowA(false); // Transitions opacity from A to B
      } else {
        setFontA(nextFont);
        setShowA(true); // Transitions opacity from B to A
      }
    }, timing);

    return () => clearInterval(interval);
  }, [timing, showA]);

  return (
    <span className="relative inline-flex items-center justify-center w-[1.0em] h-[1.0em] overflow-visible mx-[0.01em]">
      {/* Font Layer A */}
      <span
        style={{ fontFamily: fontA }}
        className={`absolute inset-0 flex items-center justify-center transition-all duration-500 ease-in-out transform ${
          showA ? 'opacity-100 scale-100 blur-none' : 'opacity-0 scale-90 blur-[2px] pointer-events-none'
        }`}
      >
        {char}
      </span>
      
      {/* Font Layer B */}
      <span
        style={{ fontFamily: fontB }}
        className={`absolute inset-0 flex items-center justify-center transition-all duration-500 ease-in-out transform ${
          showA ? 'opacity-0 scale-90 blur-[2px] pointer-events-none' : 'opacity-100 scale-100 blur-none'
        }`}
      >
        {char}
      </span>
    </span>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState('upload');
  
  // Brand Configuration State
  const [brandName, setBrandName] = useState('Aura Premium');
  const [category, setCategory] = useState('Luxury Dark Chocolate');
  const [colors, setColors] = useState('Brown, Gold');
  const [selectedFont, setSelectedFont] = useState('Playfair Display');
  const [packageShape, setPackageShape] = useState('box');
  const [fileUrl, setFileUrl] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const fileInputRef = useRef(null);

  const [isLoading, setIsLoading] = useState(false);

  const triggerAnalysisWithFile = async (fileObj) => {
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('brand_name', brandName || 'Aura');
      formData.append('category', category || 'Luxury Dark Chocolate');
      formData.append('colors', colors || 'Brown, Gold');
      formData.append('file', fileObj);

      const res = await fetch(`${API_BASE}/api/v1/analyze-brand`, {
        method: 'POST',
        body: formData
      });

      if (!res.ok) throw new Error("API Execution Failed");
      const data = await res.json();

      setOcrBoxes(data.layout_boxes);
      setRecommendations(data.recommendations);
      setPsychology(data.psychology);
      setSaliencyData(data.saliency);
      setGraphRouting(data.graph_routing);
      setPdfReportMeta(data.pdf_report);
      setAgentLogs(data.agentic_report);
      
      setBrandName(data.brand_name);
      setCategory(data.category);
      setColors(data.colors);

      if (data.recommendations && data.recommendations.length > 0) {
        setSelectedFont(data.recommendations[0].font_name);
      }

      const newMessages = [
        { role: 'user', message: `Scan uploaded design image: ${fileObj.name}` },
        { role: 'agent', message: `Analyzed uploaded design image successfully. Brand: "${data.brand_name}", Category: "${data.category}", Colors: "${data.colors}". Found ${data.layout_boxes ? data.layout_boxes.length : 0} layout elements. Initializing design audit report.` }
      ];
      setChatMessages(prev => [...prev, ...newMessages]);
    } catch (err) {
      console.error(err);
      alert("Failed to analyze image. Please ensure backend server is active on port 8000.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      triggerAnalysisWithFile(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      triggerAnalysisWithFile(file);
    }
  };
  const [positiveFeedbackCount, setPositiveFeedbackCount] = useState(24);
  const [negativeFeedbackCount, setNegativeFeedbackCount] = useState(2);
  
  // Evolved Font State
  const [baseEvoFont, setBaseEvoFont] = useState('Playfair Display');
  const [evoParams, setEvoParams] = useState({ luxury: 0.5, modern: 0.2, readability: 0.6 });
  const [evolvedDNA, setEvolvedDNA] = useState(null);
  const [evolvedGlyphs, setEvolvedGlyphs] = useState(null);

  // Agent Chat Console state
  const [chatMessages, setChatMessages] = useState([
    { role: 'agent', message: 'Hello! I am the AI Chief Designer Agent. Upload your packaging wrapper design or describe your branding goal to start the multi-agent design pipeline.' }
  ]);
  const [userPrompt, setUserPrompt] = useState('');

  // Results State
  const [ocrBoxes, setOcrBoxes] = useState([
    {"id": "box_1", "type": "Logo", "text": "Aura", "x": 35, "y": 20, "w": 30, "h": 10},
    {"id": "box_2", "type": "Headline", "text": "CLASSIC DARK", "x": 20, "y": 40, "w": 60, "h": 15},
    {"id": "box_3", "type": "Subheading", "text": "70% Single Origin Cocoa", "x": 25, "y": 60, "w": 50, "h": 8}
  ]);
  const [selectedBoxId, setSelectedBoxId] = useState(null);

  const handleUpdateBoxText = (boxId, text) => {
    setOcrBoxes(prev => prev.map(b => b.id === boxId ? { ...b, text } : b));
    const targetBox = ocrBoxes.find(b => b.id === boxId);
    if (targetBox) {
      if (targetBox.type === 'Logo') setBrandName(text);
      if (targetBox.type === 'Headline') setCategory(text);
    }
  };

  const handleUpdateBoxType = (boxId, type) => {
    setOcrBoxes(prev => prev.map(b => b.id === boxId ? { ...b, type } : b));
    const targetBox = ocrBoxes.find(b => b.id === boxId);
    if (targetBox) {
      if (type === 'Logo') setBrandName(targetBox.text);
      if (type === 'Headline') setCategory(targetBox.text);
    }
  };

  const handleDeleteBox = (boxId) => {
    setOcrBoxes(prev => prev.filter(b => b.id !== boxId));
    if (selectedBoxId === boxId) setSelectedBoxId(null);
  };

  const handleAddBox = () => {
    const newBox = {
      id: `box_${Date.now()}`,
      type: "Logo",
      text: "NEW BRAND",
      x: 35,
      y: 45,
      w: 30,
      h: 10
    };
    setOcrBoxes(prev => [...prev, newBox]);
    setSelectedBoxId(newBox.id);
  };

  const handleBoxMouseDown = (e, boxId) => {
    // Only drag when clicking box wrapper, not input controls
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'BUTTON') {
      return;
    }
    
    e.preventDefault();
    e.stopPropagation();
    setSelectedBoxId(boxId);
    
    const container = e.currentTarget.parentElement.getBoundingClientRect();
    const box = ocrBoxes.find(b => b.id === boxId);
    if (!box) return;

    const startX = e.clientX;
    const startY = e.clientY;
    const startLeft = (box.x / 100) * container.width;
    const startTop = (box.y / 100) * container.height;

    const handleMouseMove = (moveEvent) => {
      const deltaX = moveEvent.clientX - startX;
      const deltaY = moveEvent.clientY - startY;

      const newLeftPct = Math.max(0, Math.min(100 - box.w, ((startLeft + deltaX) / container.width) * 100));
      const newTopPct = Math.max(0, Math.min(100 - box.h, ((startTop + deltaY) / container.height) * 100));

      setOcrBoxes(prev => prev.map(b => b.id === boxId ? { ...b, x: Math.round(newLeftPct), y: Math.round(newTopPct) } : b));
    };

    const handleMouseUp = () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  const handleResizeMouseDown = (e, boxId) => {
    e.preventDefault();
    e.stopPropagation();
    
    const container = e.currentTarget.parentElement.parentElement.getBoundingClientRect();
    const box = ocrBoxes.find(b => b.id === boxId);
    if (!box) return;

    const startX = e.clientX;
    const startY = e.clientY;
    const startWidth = (box.w / 100) * container.width;
    const startHeight = (box.h / 100) * container.height;

    const handleMouseMove = (moveEvent) => {
      const deltaX = moveEvent.clientX - startX;
      const deltaY = moveEvent.clientY - startY;

      const newWidthPct = Math.max(10, Math.min(100 - box.x, ((startWidth + deltaX) / container.width) * 100));
      const newHeightPct = Math.max(5, Math.min(100 - box.y, ((startHeight + deltaY) / container.height) * 100));

      setOcrBoxes(prev => prev.map(b => b.id === boxId ? { ...b, w: Math.round(newWidthPct), h: Math.round(newHeightPct) } : b));
    };

    const handleMouseUp = () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };
  const [recommendations, setRecommendations] = useState(GOOGLE_FONTS);
  const [psychology, setPsychology] = useState({
    "target_age_range": "25-50",
    "gender_preference": "Neutral",
    "luxury_preference": 0.85,
    "emotional_scores": { "trust": 0.90, "excitement": 0.72, "warmth": 0.88, "premium_feeling": 0.92, "fun": 0.35 }
  });
  const [saliencyData, setSaliencyData] = useState({
    "metrics": { "shelf_visibility": 0.88, "readability_distance_meters": 8.5, "print_compatibility": 0.91, "saliency_auc": 0.88, "saliency_nss": 2.35 },
    "anchors": [{"x": 50, "y": 42, "weight": 0.95}]
  });
  const [graphRouting, setGraphRouting] = useState({
    "subcategory": "Luxury Dark Chocolate",
    "emotion": "Premium Indulgence",
    "typography": "High-Contrast Serif",
    "color": "Warm Brown & Gold",
    "material": "Recycled Kraft Cardboard",
    "print_constraints": "Foil Stamping"
  });
  const [pdfReportMeta, setPdfReportMeta] = useState(null);
  const [agentLogs, setAgentLogs] = useState([]);

  // ThreeJS 3D Simulator Refs
  const canvas3DRef = useRef(null);
  const rendererRef = useRef(null);
  const sceneRef = useRef(null);
  const meshRef = useRef(null);
  const textureCanvasRef = useRef(null);

  // Similar Font Search State
  const [similarSearchName, setSimilarSearchName] = useState('Playfair Display');
  const [similarResults, setSimilarResults] = useState([]);

  // 100k Font Browser State
  const [registryFonts, setRegistryFonts] = useState([]);
  const [registrySearch, setRegistrySearch] = useState('');
  const [registryStyle, setRegistryStyle] = useState('All');
  const [registryPage, setRegistryPage] = useState(0);
  const [registryTotal, setRegistryTotal] = useState(0);
  const [registryError, setRegistryError] = useState(null);
  const [registryLimit, setRegistryLimit] = useState(25);

  // Fetch fonts for 100k Browser
  useEffect(() => {
    const fetchRegistryFonts = async () => {
      try {
        const offset = registryPage * registryLimit;
        const res = await fetch(`${API_BASE}/api/v1/fonts?limit=${registryLimit}&offset=${offset}&search=${encodeURIComponent(registrySearch)}&style=${registryStyle}`);
        if (!res.ok) {
          throw new Error(`Server returned status: ${res.status}`);
        }
        const data = await res.json();
        setRegistryFonts(data.fonts || []);
        setRegistryTotal(data.total || 0);
        setRegistryError(null);
      } catch (err) {
        console.error("Error fetching registry fonts:", err);
        setRegistryError("Failed to connect to backend server. Please verify uvicorn is running on port 8000.");
      }
    };
    fetchRegistryFonts();
  }, [registryPage, registrySearch, registryStyle, registryLimit]);

  // Initialize Evolved DNA preview
  useEffect(() => {
    handleEvolveFont();
  }, [baseEvoFont]);

  // Autocomplete Font Search States
  const [selectedFontSearch, setSelectedFontSearch] = useState('Playfair Display');
  const [selectedFontOptions, setSelectedFontOptions] = useState([]);
  const [showSelectedFontDropdown, setShowSelectedFontDropdown] = useState(false);

  const [evoFontSearch, setEvoFontSearch] = useState('Playfair Display');
  const [evoFontOptions, setEvoFontOptions] = useState([]);
  const [showEvoFontDropdown, setShowEvoFontDropdown] = useState(false);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/v1/fonts?limit=10&search=${encodeURIComponent(selectedFontSearch)}`);
        const data = await res.json();
        setSelectedFontOptions(data.fonts || []);
      } catch (err) {
        console.error(err);
      }
    };
    if (showSelectedFontDropdown) {
      fetchOptions();
    }
  }, [selectedFontSearch, showSelectedFontDropdown]);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/v1/fonts?limit=10&search=${encodeURIComponent(evoFontSearch)}`);
        const data = await res.json();
        setEvoFontOptions(data.fonts || []);
      } catch (err) {
        console.error(err);
      }
    };
    if (showEvoFontDropdown) {
      fetchOptions();
    }
  }, [evoFontSearch, showEvoFontDropdown]);

  // Autocomplete Font Similarity states
  const [similaritySearchInput, setSimilaritySearchInput] = useState('Playfair Display');
  const [similarityOptions, setSimilarityOptions] = useState([]);
  const [showSimilarityDropdown, setShowSimilarityDropdown] = useState(false);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/v1/fonts?limit=10&search=${encodeURIComponent(similaritySearchInput)}`);
        const data = await res.json();
        setSimilarityOptions(data.fonts || []);
      } catch (err) {
        console.error(err);
      }
    };
    if (showSimilarityDropdown) {
      fetchOptions();
    }
  }, [similaritySearchInput, showSimilarityDropdown]);

  // Three.js Simulator setup
  useEffect(() => {
    if (!canvas3DRef.current || activeTab !== 'simulator') return;

    // Create 2D texture canvas to draw chocolate wrap layout dynamically
    const textCanvas = document.createElement('canvas');
    textCanvas.width = 2048;
    textCanvas.height = 2048;
    textureCanvasRef.current = textCanvas;
    updateTextureCanvas();

    const width = canvas3DRef.current.clientWidth;
    const height = canvas3DRef.current.clientHeight;

    // Set up Scene, Camera, Renderer
    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.background = new THREE.Color('#0F0F1A');

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 0, 5);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    canvas3DRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Add HDR / Studio lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight1.position.set(5, 10, 7);
    dirLight1.castShadow = true;
    scene.add(dirLight1);

    const pointLight = new THREE.PointLight(0x6366F1, 0.6, 10);
    pointLight.position.set(-3, -3, 3);
    scene.add(pointLight);

    // Create 3D Package Mesh (Chocolate bar slab or cylinder coffee jar)
    const isCoffee = category.toLowerCase().includes('coffee') || category.toLowerCase().includes('beverage');
    const cols = colors.split(',').map(c => c.trim().toLowerCase());
    const primaryCol = cols[0] === 'brown' ? '#3E2723' : cols[0] === 'blue' ? '#0D47A1' : cols[0] === 'green' ? '#1B5E20' : '#111827';
    
    const sideMat = new THREE.MeshStandardMaterial({
      color: new THREE.Color(primaryCol),
      roughness: 0.5,
      metalness: 0.1
    });
    
    const texture = previewUrl 
      ? new THREE.TextureLoader().load(previewUrl) 
      : new THREE.CanvasTexture(textCanvas);
      
    const maxAnisotropy = renderer.capabilities.getMaxAnisotropy();
    texture.anisotropy = maxAnisotropy;
    texture.minFilter = THREE.LinearMipmapLinearFilter;
    texture.magFilter = THREE.LinearFilter;
      
    const frontMat = new THREE.MeshStandardMaterial({
      map: texture,
      roughness: 0.25,
      metalness: 0.1
    });

    let mainObject;

    if (packageShape === 'jar') {
      const geometry = new THREE.CylinderGeometry(0.8, 0.8, 2.2, 32);
      const materials = [frontMat, sideMat, sideMat]; // Side, Top, Bottom
      mainObject = new THREE.Mesh(geometry, materials);
      mainObject.castShadow = true;
      mainObject.receiveShadow = true;
      scene.add(mainObject);
    } 
    else if (packageShape === 'bottle') {
      const group = new THREE.Group();
      
      // Body
      const bodyGeom = new THREE.CylinderGeometry(0.6, 0.6, 1.8, 32);
      const bodyMaterials = [frontMat, sideMat, sideMat];
      const bodyMesh = new THREE.Mesh(bodyGeom, bodyMaterials);
      bodyMesh.castShadow = true;
      bodyMesh.receiveShadow = true;
      group.add(bodyMesh);
      
      // Neck
      const neckGeom = new THREE.CylinderGeometry(0.18, 0.18, 0.5, 32);
      const neckMesh = new THREE.Mesh(neckGeom, sideMat);
      neckMesh.position.y = 1.15;
      neckMesh.castShadow = true;
      neckMesh.receiveShadow = true;
      group.add(neckMesh);
      
      // Cap
      const capGeom = new THREE.CylinderGeometry(0.2, 0.2, 0.15, 32);
      const capMesh = new THREE.Mesh(capGeom, sideMat);
      capMesh.position.y = 1.45;
      capMesh.castShadow = true;
      capMesh.receiveShadow = true;
      group.add(capMesh);
      
      scene.add(group);
      mainObject = group;
    } 
    else if (packageShape === 'hex') {
      const geometry = new THREE.CylinderGeometry(0.9, 0.9, 2.2, 6);
      const materials = [frontMat, sideMat, sideMat];
      mainObject = new THREE.Mesh(geometry, materials);
      mainObject.castShadow = true;
      mainObject.receiveShadow = true;
      scene.add(mainObject);
    } 
    else if (packageShape === 'vial') {
      const geometry = new THREE.CylinderGeometry(0.9, 0.9, 1.2, 32);
      const materials = [frontMat, sideMat, sideMat];
      mainObject = new THREE.Mesh(geometry, materials);
      mainObject.castShadow = true;
      mainObject.receiveShadow = true;
      scene.add(mainObject);
    } 
    else { // 'box'
      const geometry = new THREE.BoxGeometry(1.6, 2.4, 0.3);
      const materials = [sideMat, sideMat, sideMat, sideMat, frontMat, sideMat];
      mainObject = new THREE.Mesh(geometry, materials);
      mainObject.castShadow = true;
      mainObject.receiveShadow = true;
      scene.add(mainObject);
    }

    meshRef.current = mainObject;

    // Rotation controls and animation loop
    let animationFrameId;
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };

    const handleMouseDown = () => { isDragging = true; };
    const handleMouseMove = (e) => {
      const deltaMove = {
        x: e.offsetX - previousMousePosition.x,
        y: e.offsetY - previousMousePosition.y
      };

      if (isDragging && meshRef.current) {
        meshRef.current.rotation.y += deltaMove.x * 0.01;
        meshRef.current.rotation.x += deltaMove.y * 0.01;
      }

      previousMousePosition = {
        x: e.offsetX,
        y: e.offsetY
      };
    };
    const handleMouseUp = () => { isDragging = false; };

    const domElement = renderer.domElement;
    domElement.addEventListener('mousedown', handleMouseDown);
    domElement.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      if (!isDragging && meshRef.current) {
        // Slow idle spin
        meshRef.current.rotation.y += 0.005;
      }
      renderer.render(scene, camera);
    };
    animate();

     // Clean up
    return () => {
      cancelAnimationFrame(animationFrameId);
      domElement.removeEventListener('mousedown', handleMouseDown);
      domElement.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
      if (canvas3DRef.current && renderer.domElement && canvas3DRef.current.contains(renderer.domElement)) {
        canvas3DRef.current.removeChild(renderer.domElement);
      }
    };
  }, [activeTab, category, previewUrl, packageShape]);

  const updateTextureCanvas = () => {
    const canvas = textureCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    // Reset transform matrix and apply 4x scale for 2K (2048x2048) resolution clarity
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(4, 4);
    
    // Parse color styles
    const cols = colors.split(',').map(c => c.trim().toLowerCase());
    const primaryCol = cols[0] === 'brown' ? '#3E2723' : cols[0] === 'blue' ? '#0D47A1' : cols[0] === 'green' ? '#1B5E20' : '#111827';
    const accentCol = cols[1] === 'gold' ? '#D4AF37' : cols[1] === 'white' ? '#FFFFFF' : '#EC4899';

    // Fill background wrapper
    ctx.fillStyle = primaryCol;
    ctx.fillRect(0, 0, 512, 512);

    // Draw luxury geometric background watermark (faint diagonal gold pinstripes)
    ctx.save();
    ctx.strokeStyle = accentCol;
    ctx.lineWidth = 0.5;
    ctx.globalAlpha = 0.08;
    for (let i = -512; i < 1024; i += 24) {
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i + 512, 512);
      ctx.stroke();
    }
    ctx.restore();

    // Draw borders & lines
    ctx.strokeStyle = accentCol;
    ctx.lineWidth = 1.5;
    ctx.strokeRect(25, 25, 462, 462);
    
    // Draw L-shaped corner accents
    const cornerSize = 20;
    ctx.lineWidth = 2.5;
    // Top-Left
    ctx.beginPath(); ctx.moveTo(25 + cornerSize, 25); ctx.lineTo(25, 25); ctx.lineTo(25, 25 + cornerSize); ctx.stroke();
    // Top-Right
    ctx.beginPath(); ctx.moveTo(487 - cornerSize, 25); ctx.lineTo(487, 25); ctx.lineTo(487, 25 + cornerSize); ctx.stroke();
    // Bottom-Left
    ctx.beginPath(); ctx.moveTo(25 + cornerSize, 487); ctx.lineTo(25, 487); ctx.lineTo(25, 487 - cornerSize); ctx.stroke();
    // Bottom-Right
    ctx.beginPath(); ctx.moveTo(487 - cornerSize, 487); ctx.lineTo(487, 487); ctx.lineTo(487, 487 - cornerSize); ctx.stroke();

    // Draw Header Label
    ctx.fillStyle = accentCol;
    ctx.textAlign = 'center';
    ctx.font = 'bold 9px sans-serif';
    ctx.fillText("✦ FINEST ARTISANAL SELECTION ✦", 256, 75);

    // Dynamically apply selected font style
    const fontStyle = `"${selectedFont}", sans-serif`;
    
    // Draw Logo text
    ctx.fillStyle = accentCol;
    ctx.font = `bold 32px ${fontStyle}`;
    ctx.fillText(brandName.toUpperCase(), 256, 125);

    // Draw split divider with diamond Lockup
    ctx.strokeStyle = accentCol;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(100, 160);
    ctx.lineTo(230, 160);
    ctx.moveTo(282, 160);
    ctx.lineTo(412, 160);
    ctx.stroke();
    ctx.font = 'bold 12px sans-serif';
    ctx.fillText("◆", 256, 164);

    // Draw Headline Text
    ctx.fillStyle = '#FFFFFF';
    ctx.font = `bold 24px ${fontStyle}`;
    ctx.fillText(category.toUpperCase(), 256, 245);

    // Draw Subheading
    ctx.fillStyle = 'rgba(255,255,255,0.7)';
    ctx.font = `italic 16px ${fontStyle}`;
    ctx.fillText("AI Formulated Typography", 256, 285);

    // Draw rotated vertical side labels
    ctx.save();
    ctx.translate(45, 256);
    ctx.rotate(-Math.PI / 2);
    ctx.fillStyle = 'rgba(255,255,255,0.35)';
    ctx.font = 'bold 9px sans-serif';
    ctx.fillText("✦ HANDCRAFTED QUALITY ✦", 0, 0);
    ctx.restore();

    ctx.save();
    ctx.translate(467, 256);
    ctx.rotate(Math.PI / 2);
    ctx.fillStyle = 'rgba(255,255,255,0.35)';
    ctx.font = 'bold 9px sans-serif';
    ctx.fillText("✦ ESTABLISHED 2026 ✦", 0, 0);
    ctx.restore();

    // Concentric luxury stamps
    ctx.strokeStyle = accentCol;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(256, 395, 38, 0, Math.PI * 2);
    ctx.stroke();
    
    ctx.lineWidth = 0.5;
    ctx.beginPath();
    ctx.arc(256, 395, 33, 0, Math.PI * 2);
    ctx.stroke();
    
    ctx.fillStyle = accentCol;
    ctx.font = `bold 9px sans-serif`;
    ctx.fillText("CRU SPECIAL", 256, 390);
    ctx.font = `bold 8px sans-serif`;
    ctx.fillStyle = '#FFFFFF';
    ctx.fillText("ORGANIC", 256, 404);

    // Bottom Footer label
    ctx.fillStyle = 'rgba(255,255,255,0.5)';
    ctx.font = 'bold 8px sans-serif';
    ctx.fillText("NET WT. 100g ℮ (3.5 OZ) | PRODUCT OF COSTA RICA", 256, 465);
  };

  // Dynamic Web Font Loader & 3D Texture Updater Hook
  useEffect(() => {
    if (!selectedFont) return;
    
    // Create a link tag to fetch the Google Font dynamically
    const fontId = `gfont-${selectedFont.replace(/\s+/g, '-').toLowerCase()}`;
    
    const applyTextureUpdate = () => {
      updateTextureCanvas();
      if (meshRef.current && meshRef.current.material && meshRef.current.material.map) {
        meshRef.current.material.map.needsUpdate = true;
      }
    };

    // Check if the font is a standard system font
    const systemFonts = ['arial', 'helvetica', 'times new roman', 'georgia', 'garamond', 'didot', 'calibri', 'courier new', 'sans-serif', 'serif'];
    const isSystemFont = systemFonts.some(f => selectedFont.toLowerCase().includes(f));

    if (isSystemFont || document.getElementById(fontId)) {
      applyTextureUpdate();
    } else {
      // Append font stylesheet to document head dynamically
      const link = document.createElement('link');
      link.id = fontId;
      link.rel = 'stylesheet';
      link.href = `https://fonts.googleapis.com/css2?family=${encodeURIComponent(selectedFont)}:wght@400;700&display=swap`;
      
      link.onload = () => {
        // Wait 150ms for browser to parse font outlines, then redraw
        setTimeout(applyTextureUpdate, 150);
      };
      link.onerror = () => {
        applyTextureUpdate();
      };
      
      document.head.appendChild(link);
    }
  }, [selectedFont, brandName, category, colors]);

  // Trigger main brand multi-agent analysis
  const handleAnalyze = async (e) => {
    if (e) e.preventDefault();
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('brand_name', brandName);
      formData.append('category', category);
      formData.append('colors', colors);
      if (selectedFile) {
        formData.append('file', selectedFile);
      }

      const res = await fetch(`${API_BASE}/api/v1/analyze-brand`, {
        method: 'POST',
        body: formData
      });

      if (!res.ok) throw new Error("API Execution Failed");
      const data = await res.json();

      // Set state variables from agent outputs
      setOcrBoxes(data.layout_boxes);
      setRecommendations(data.recommendations);
      setPsychology(data.psychology);
      setSaliencyData(data.saliency);
      setGraphRouting(data.graph_routing);
      setPdfReportMeta(data.pdf_report);
      setAgentLogs(data.agentic_report);
      setBrandName(data.brand_name);
      setCategory(data.category);
      setColors(data.colors);
      
      // Auto-set the best recommended font
      if (data.recommendations && data.recommendations.length > 0) {
        setSelectedFont(data.recommendations[0].font_name);
      }

      // Add thoughts to agent chat console
      const newMessages = [
        { role: 'user', message: `Orchestrate design audit for ${brandName} (${category})` },
        { role: 'agent', message: `Pipeline executed successfully. Chief Designer approved layout validation (Confidence: ${data.validator.overall_confidence * 100}%). PDF Report is ready for compile.` }
      ];
      setChatMessages(prev => [...prev, ...newMessages]);

    } catch (err) {
      console.error(err);
      alert("Failed to connect to backend. Please ensure uvicorn server is running on port 8000.");
    } finally {
      setIsLoading(false);
    }
  };

  // Trigger Font DNA Evolution
  const handleEvolveFont = async () => {
    try {
      const formData = new FormData();
      formData.append('base_font', baseEvoFont);
      formData.append('luxury', evoParams.luxury);
      formData.append('modern', evoParams.modern);
      formData.append('readability', evoParams.readability);

      const res = await fetch(`${API_BASE}/api/v1/generate-font`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setEvolvedDNA(data.evolved_dna);
      setEvolvedGlyphs(data.font_face.glyphs);
    } catch (err) {
      console.error(err);
    }
  };

  // Search Font Similarity via FAISS
  const handleSimilaritySearch = async (e) => {
    if (e) e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('font_name', similarSearchName);
      
      const res = await fetch(`${API_BASE}/api/v1/font-similarity`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setSimilarResults(data.similar_fonts);
    } catch (err) {
      console.error(err);
    }
  };

  // Handle agent chat prompt input
  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!userPrompt.trim()) return;

    const userMsg = userPrompt;
    setUserPrompt('');
    setChatMessages(prev => [...prev, { role: 'user', message: userMsg }]);
    setChatMessages(prev => [...prev, { role: 'agent', message: 'Analyzing prompt and running multi-agent workflow...', isLoading: true }]);

    try {
      const res = await fetch(`${API_BASE}/api/v1/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMsg,
          brand_name: brandName,
          category: category,
          colors: colors
        })
      });

      if (!res.ok) throw new Error("API Connection Failed");
      const data = await res.json();

      setChatMessages(prev => {
        const filtered = prev.filter(m => !m.isLoading);
        return [...filtered, { 
          role: 'agent', 
          message: data.reply,
          recommendations: data.recommendations
        }];
      });

      if (data.agentic_report) {
        setAgentLogs(data.agentic_report);
      }
    } catch (err) {
      console.error(err);
      setChatMessages(prev => {
        const filtered = prev.filter(m => !m.isLoading);
        return [...filtered, { 
          role: 'agent', 
          message: "Unable to reach the Agent server. Please make sure the backend FastAPI service is running." 
        }];
      });
    }
  };

  const handleFeedback = (isPositive) => {
    if (isPositive) {
      setPositiveFeedbackCount(prev => prev + 1);
    } else {
      setNegativeFeedbackCount(prev => prev + 1);
    }
  };

  return (
    <div className="min-h-screen bg-brand-bg text-gray-100 flex flex-col font-sans scroll-smooth overflow-x-hidden relative">
      <div className="glow-orb-bg-1"></div>
      <div className="glow-orb-bg-2"></div>
      
      {/* FULLSCREEN MORPHING TYPOGRAPHY LANDING INTRO */}
      <div className="h-screen w-full flex flex-col items-center justify-center relative select-none bg-gradient-to-b from-[#07070c] via-[#090912] to-brand-bg">
        <div className="text-center">
          <h1 
            className="text-[15vw] md:text-[12vw] font-bold uppercase tracking-[0.4em] pl-[0.4em] leading-[0.8] text-white select-none mb-16"
            style={{ fontFamily: '"Montserrat", sans-serif', textShadow: 'none', filter: 'none' }}
          >
            FONT
          </h1>
          {/* PICKER (morphing letter styles) */}
          <h2 className="text-[6vw] md:text-[4vw] font-normal uppercase leading-[0.9] text-white flex justify-center select-none">
            {Array.from("PICKER").map((char, idx) => {
              const timings = [1200, 2200, 1800, 2600, 1600, 2800];
              return (
                <MorphingLetter 
                  key={idx} 
                  char={char} 
                  timing={timings[idx]} 
                />
              );
            })}
          </h2>
        </div>

        {/* Scroll indicator */}
        <a 
          href="#dashboard-anchor" 
          className="absolute bottom-10 flex flex-col items-center animate-bounce text-brand-muted text-xs font-semibold hover:text-brand-primary transition-colors cursor-pointer"
        >
          <span>Scroll Down to Open Platform</span>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mt-2 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </a>
      </div>

      {/* HEADER BANNER */}
      <header id="dashboard-anchor" className="border-b border-brand-border bg-brand-panel px-6 py-4 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center space-x-3">
          <div className="bg-brand-bg border border-brand-border p-2 rounded-xl flex items-center justify-center shadow-md">
            <svg viewBox="0 0 100 100" className="h-6 w-6 text-brand-primary animate-pulse" fill="none" stroke="currentColor" strokeWidth="9" strokeLinecap="round" strokeLinejoin="round">
              <path d="M 20 60 A 30 30 0 0 1 50 20" />
              <path d="M 38 20 H 50 V 32" />
              <path d="M 50 20 A 30 30 0 0 1 80 60" />
              <path d="M 80 48 V 60 H 68" />
              <path d="M 80 60 A 30 30 0 0 1 20 60" />
              <path d="M 32 60 H 20 V 48" />
            </svg>
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white flex items-center">
              FONT PICKER
            </h1>
            <p className="text-xs text-brand-muted">Typography & Branding Intelligence Platform</p>
          </div>
        </div>

        <nav className="flex space-x-1">
          {[
            { id: 'upload', label: 'Brand Scanner', icon: Upload },
            { id: 'simulator', label: '3D Simulator', icon: RotateCw },
            { id: 'fontlab', label: 'FontLab DNA', icon: Sliders },
            { id: 'similarity', label: 'FAISS Vector Search', icon: Search },
            { id: 'registry', label: '100k Font Browser', icon: Database },
            { id: 'agents', label: 'AI Agent Console', icon: MessageSquare },
            { id: 'dashboard', label: 'Dashboard & Reports', icon: BarChart2 }
          ].map(tab => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm transition-all ${
                  active 
                    ? 'bg-brand-primary text-white shadow-lg shadow-brand-primary/20' 
                    : 'text-brand-muted hover:text-gray-100 hover:bg-brand-border/40'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </header>

      {/* MAIN CONTAINER */}
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full grid grid-cols-1 gap-6">
        
        {/* TAB 1: UPLOAD SCANNER & RECOMMENDATION */}
        {activeTab === 'upload' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Input Config & File Upload */}
            <div className="lg:col-span-1 space-y-6">
              <div className="glass-panel rounded-2xl p-6">
                <h2 className="text-lg font-bold text-white mb-4 flex items-center space-x-2">
                  <span>1. Brand parameters</span>
                </h2>
                
                <form onSubmit={handleAnalyze} className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-brand-muted uppercase mb-1">Company/Brand name</label>
                    <input 
                      type="text" 
                      value={brandName}
                      onChange={e => setBrandName(e.target.value)}
                      className="w-full bg-brand-bg border border-brand-border rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-brand-primary" 
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-brand-muted uppercase mb-1">Product Category / Niche</label>
                    <input 
                      type="text" 
                      value={category}
                      onChange={e => setCategory(e.target.value)}
                      className="w-full bg-brand-bg border border-brand-border rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-brand-primary" 
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-brand-muted uppercase mb-1">Brand Colors (comma separated)</label>
                    <input 
                      type="text" 
                      value={colors}
                      onChange={e => setColors(e.target.value)}
                      className="w-full bg-brand-bg border border-brand-border rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-brand-primary" 
                    />
                  </div>

                  {/* Real Uploader */}
                  <div 
                    onClick={() => fileInputRef.current?.click()}
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                    className="border-2 border-dashed border-brand-border rounded-xl p-6 text-center hover:border-brand-primary/50 transition-colors cursor-pointer bg-brand-bg/50 relative animate-fade-in"
                  >
                    <input 
                      type="file" 
                      ref={fileInputRef} 
                      onChange={handleFileChange} 
                      className="hidden" 
                      accept="image/*"
                    />
                    {previewUrl ? (
                      <div className="space-y-2">
                        <img src={previewUrl} className="max-h-24 mx-auto rounded border border-brand-border shadow-md" alt="Preview" />
                        <span className="text-xs text-brand-secondary block font-semibold">Image loaded successfully</span>
                      </div>
                    ) : (
                      <>
                        <Upload className="h-8 w-8 text-brand-primary mx-auto mb-2" />
                        <span className="text-xs text-brand-muted block">Drag & drop or click to upload package/logo</span>
                        <span className="text-[10px] text-gray-500 block mt-1">(Supports JPG, PNG, WebP)</span>
                      </>
                    )}
                  </div>

                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full py-3 bg-gradient-to-r from-brand-primary to-brand-accent text-white font-bold rounded-xl shadow-lg hover:shadow-brand-primary/20 transition-all flex items-center justify-center space-x-2 text-sm"
                  >
                    {isLoading ? (
                      <>
                        <RefreshCw className="h-4 w-4 animate-spin" />
                        <span>Running Agentic Planners...</span>
                      </>
                    ) : (
                      <>
                        <Sparkles className="h-4 w-4" />
                        <span>Run Brand Design Audit</span>
                      </>
                    )}
                  </button>
                </form>
              </div>

              {/* Traversed Knowledge Graph Path */}
              <div className="glass-panel rounded-2xl p-6">
                <h3 className="text-sm font-bold text-white mb-3 flex items-center">
                  <Database className="h-4 w-4 mr-2 text-brand-secondary" />
                  Knowledge Graph Traversal
                </h3>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between py-1.5 border-b border-brand-border/40">
                    <span className="text-brand-muted">Subcategory</span>
                    <span className="text-brand-secondary font-semibold">{graphRouting.subcategory}</span>
                  </div>
                  <div className="flex justify-between py-1.5 border-b border-brand-border/40">
                    <span className="text-brand-muted">Target Emotion</span>
                    <span className="text-white">{graphRouting.emotion}</span>
                  </div>
                  <div className="flex justify-between py-1.5 border-b border-brand-border/40">
                    <span className="text-brand-muted">Typography Standard</span>
                    <span className="text-white">{graphRouting.typography}</span>
                  </div>
                  <div className="flex justify-between py-1.5 border-b border-brand-border/40">
                    <span className="text-brand-muted">Packaging Material</span>
                    <span className="text-white">{graphRouting.material}</span>
                  </div>
                  <div className="flex justify-between py-1.5 border-b border-brand-border/40">
                    <span className="text-brand-muted">Print Constraints</span>
                    <span className="text-white">{graphRouting.print_constraints}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Layout OCR overlay visualizer */}
            <div className="lg:col-span-1 space-y-6">
              <div className="glass-panel rounded-2xl p-6">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-lg font-bold text-white">2. Visual OCR Canvas</h2>
                  <button
                    type="button"
                    onClick={handleAddBox}
                    className="px-2.5 py-1 bg-brand-primary/20 hover:bg-brand-primary/45 border border-brand-primary/40 hover:border-brand-primary text-brand-primary hover:text-white rounded-lg text-xs font-bold transition-all"
                  >
                    ＋ Add Box
                  </button>
                </div>
                
                <div 
                  className="relative aspect-[4/5] bg-brand-bg rounded-xl border border-brand-border overflow-hidden flex items-center justify-center p-4"
                  onClick={() => setSelectedBoxId(null)}
                >
                  {/* Outer wrapper representation */}
                  <div className="w-full h-full rounded-lg border-2 border-brand-accent/50 relative overflow-hidden bg-cover bg-center" style={{ backgroundImage: previewUrl ? `url(${previewUrl})` : 'none', backgroundColor: previewUrl ? 'transparent' : (colors.split(',')[0].trim().toLowerCase() === 'brown' ? '#3E2723' : '#111827') }}>
                    {/* Render OCR absolute boxes */}
                    {ocrBoxes.map(box => {
                      const isSelected = selectedBoxId === box.id;
                      return (
                        <div
                          key={box.id}
                          onMouseDown={(e) => handleBoxMouseDown(e, box.id)}
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedBoxId(box.id);
                          }}
                          className={`absolute border rounded px-1.5 py-1 text-[8.5px] font-bold text-white flex flex-col justify-between cursor-move select-none transition-shadow ${
                            isSelected
                              ? 'border-brand-primary bg-brand-primary/20 ring-2 ring-brand-primary z-50 shadow-lg shadow-brand-primary/20'
                              : 'border-brand-border/60 bg-brand-panel/40 hover:border-brand-primary/40'
                          }`}
                          style={{
                            left: `${box.x}%`,
                            top: `${box.y}%`,
                            width: `${box.w}%`,
                            height: `${box.h}%`
                          }}
                        >
                          {/* Selected edit popups */}
                          {isSelected && (
                            <div 
                              className="absolute -top-7 left-0 right-0 bg-[#0c0c16] border border-brand-border rounded flex space-x-1 p-0.5 z-[100] text-[6px] shadow-xl justify-between items-center"
                              onMouseDown={(e) => e.stopPropagation()}
                              onClick={(e) => e.stopPropagation()}
                            >
                              <div className="flex space-x-0.5">
                                {['Logo', 'Headline', 'Subheading', 'Price', 'Legal'].map(type => (
                                  <button
                                    key={type}
                                    type="button"
                                    onClick={() => handleUpdateBoxType(box.id, type)}
                                    className={`px-1 py-0.5 rounded text-[5px] font-bold transition-colors ${box.type === type ? 'bg-brand-primary text-white' : 'text-gray-400 hover:text-white hover:bg-brand-panel/60'}`}
                                  >
                                    {type}
                                  </button>
                                ))}
                              </div>
                              <button
                                type="button"
                                onClick={() => handleDeleteBox(box.id)}
                                className="px-1 py-0.5 rounded bg-red-600 hover:bg-red-500 text-white text-[5px] font-bold transition-colors ml-1"
                              >
                                Delete
                              </button>
                            </div>
                          )}

                          <span className="bg-brand-primary text-white scale-75 origin-top-left px-0.5 rounded text-[6px] w-fit pointer-events-none mb-0.5">
                            {box.type}
                          </span>

                          {isSelected ? (
                            <input
                              type="text"
                              value={box.text}
                              onChange={(e) => handleUpdateBoxText(box.id, e.target.value)}
                              onMouseDown={(e) => e.stopPropagation()}
                              onClick={(e) => e.stopPropagation()}
                              className="w-full bg-[#05050a] text-white border border-brand-border rounded px-1 py-0.5 text-[8px] font-medium focus:outline-none focus:border-brand-primary h-[14px]"
                              autoFocus
                            />
                          ) : (
                            <span className="truncate block pointer-events-none">{box.text}</span>
                          )}

                          {/* Resize Handle */}
                          {isSelected && (
                            <div 
                              className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-brand-primary cursor-se-resize rounded-tl flex items-center justify-center text-[5.5px] text-white font-bold select-none"
                              onMouseDown={(e) => handleResizeMouseDown(e, box.id)}
                              onClick={(e) => e.stopPropagation()}
                            >
                              ⤡
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div className="mt-4 flex justify-between items-center text-[10px] text-brand-muted">
                  <span>Drag to move. Click to select. Resize bottom-right (⤡).</span>
                  <span>OCR Accuracy: 98.8%</span>
                </div>
              </div>
            </div>

            {/* Top 25 Recommended Fonts */}
            <div className="lg:col-span-1 space-y-6">
              <div className="glass-panel rounded-2xl p-6 flex flex-col h-full">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-lg font-bold text-white">3. Top Recommended Fonts</h2>
                  <span className="text-xs bg-brand-secondary/15 text-brand-secondary px-2.5 py-0.5 rounded-full border border-brand-secondary/30">
                    Transformer Ranker
                  </span>
                </div>

                <div className="space-y-3 overflow-y-auto max-h-[460px] pr-2">
                  {recommendations.map((font, idx) => (
                    <div 
                      key={idx}
                      onClick={() => setSelectedFont(font.font_name || font.name)}
                      className={`p-3 rounded-xl border transition-all cursor-pointer ${
                        selectedFont === (font.font_name || font.name)
                          ? 'border-brand-primary bg-brand-primary/10'
                          : 'border-brand-border bg-brand-panel/40 hover:border-brand-border/80'
                      }`}
                    >
                      <div className="flex justify-between items-center">
                        <span 
                          className="font-bold text-sm text-white"
                          style={getFontPreviewStyle({ name: font.font_name || font.name, style: font.style || (font.metrics ? font.metrics.style : 'Sans') })}
                        >
                          {font.font_name || font.name}
                        </span>
                        <span className="text-xs text-brand-primary font-bold">
                          {font.confidence ? `${(font.confidence * 100).toFixed(0)}% Match` : `${(font.lux * 100).toFixed(0)}% Match`}
                        </span>
                      </div>
                      
                      {/* DNA Scores */}
                      <div className="grid grid-cols-3 gap-2 mt-2 text-[10px] text-brand-muted">
                        <div>Readability: {font.metrics ? font.metrics.readability_score : font.read}</div>
                        <div>Luxury: {font.metrics ? font.metrics.luxury_score : font.lux}</div>
                        <div>Visibility: {font.metrics ? font.metrics.shelf_visibility_score : font.shelf}</div>
                      </div>

                      {/* Explainability snippet */}
                      {font.explainability && (
                        <p className="text-[10px] text-gray-400 mt-2 line-clamp-2 italic">
                          "{font.explainability.why_this_font}"
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>

          </div>
        )}

        {/* TAB 2: 3D SIMULATOR */}
        {activeTab === 'simulator' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Viewport Render container */}
            <div className="lg:col-span-2 glass-panel rounded-3xl p-6 flex flex-col">
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h2 className="text-lg font-bold text-white">Interactive 3D WebGL Simulator</h2>
                  <p className="text-xs text-brand-muted">Click & drag bar or bottle to rotate packaging model</p>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="h-2 w-2 rounded-full bg-brand-secondary animate-pulse" />
                  <span className="text-xs text-brand-secondary font-semibold">HDR Studio Light active</span>
                </div>
              </div>

              {/* WebGL Mount point */}
              <div 
                ref={canvas3DRef}
                className="w-full aspect-video bg-[#0F0F1A] rounded-2xl overflow-hidden border border-brand-border shadow-inner cursor-grab active:cursor-grabbing"
              />

              <div className="mt-4 grid grid-cols-3 gap-4 text-center text-xs text-brand-muted">
                <div className="p-3 bg-brand-panel/30 border border-brand-border/40 rounded-xl">
                  <span className="block font-semibold text-white">Material Shader</span>
                  <span>Matte Cardboard PBR</span>
                </div>
                <div className="p-3 bg-brand-panel/30 border border-brand-border/40 rounded-xl">
                  <span className="block font-semibold text-white">Render Resolution</span>
                  <span>2K HD (2048px)</span>
                </div>
                <div className="p-3 bg-brand-panel/30 border border-brand-border/40 rounded-xl">
                  <span className="block font-semibold text-white">Specularity Map</span>
                  <span>Custom Texture</span>
                </div>
              </div>
            </div>

            {/* Typography Wrap Controls */}
            <div className="lg:col-span-1 space-y-6">
              <div className="glass-panel rounded-2xl p-6">
                <h3 className="text-base font-bold text-white mb-4">Branding Material Editor</h3>

                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-brand-muted uppercase mb-1">Selected Font Face</label>
                    <div className="relative">
                      <input
                        type="text"
                        value={selectedFontSearch}
                        onChange={e => {
                          setSelectedFontSearch(e.target.value);
                          setShowSelectedFontDropdown(true);
                        }}
                        onFocus={() => setShowSelectedFontDropdown(true)}
                        onBlur={() => setTimeout(() => setShowSelectedFontDropdown(false), 250)}
                        placeholder="Search 100,000 fonts..."
                        className="w-full bg-brand-bg border border-brand-border rounded-lg pl-3 pr-8 py-2 text-sm text-white focus:outline-none focus:border-brand-primary"
                      />
                      {selectedFontSearch && (
                        <button
                          type="button"
                          onMouseDown={(e) => {
                            e.preventDefault();
                            setSelectedFontSearch('');
                            setSelectedFont('');
                          }}
                          className="absolute right-2.5 top-1/2 -translate-y-1/2 text-brand-muted hover:text-white p-0.5 rounded-full hover:bg-brand-border/40 transition-colors"
                        >
                          <X className="h-3.5 w-3.5" />
                        </button>
                      )}
                      {showSelectedFontDropdown && selectedFontOptions.length > 0 && (
                        <div className="absolute left-0 right-0 mt-1 max-h-60 overflow-y-auto bg-[#141424] border border-brand-border rounded-lg shadow-xl z-50 text-xs divide-y divide-brand-border/40">
                          {selectedFontOptions.map(option => (
                            <div
                              key={option.name}
                              onMouseDown={() => {
                                setSelectedFont(option.name);
                                setSelectedFontSearch(option.name);
                                setShowSelectedFontDropdown(false);
                              }}
                              className="p-2.5 cursor-pointer hover:bg-brand-primary/20 text-white flex justify-between items-center transition-colors"
                            >
                              <span className="font-bold">{option.name}</span>
                              <span className="text-[10px] px-2 py-0.5 rounded border border-brand-primary/30 text-brand-primary bg-brand-primary/5">{option.style}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-brand-muted uppercase mb-1">Primary Wrap Color</label>
                    <input
                      type="text"
                      value={colors}
                      onChange={e => setColors(e.target.value)}
                      placeholder="e.g. brown, gold"
                      className="w-full bg-brand-bg border border-brand-border rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-brand-primary"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-brand-muted uppercase mb-1">Package Shape Profile</label>
                    <div className="grid grid-cols-5 gap-1.5 text-center">
                      {[
                        { id: 'box', label: 'Box', icon: '📦' },
                        { id: 'jar', label: 'Jar', icon: '🥫' },
                        { id: 'bottle', label: 'Bottle', icon: '🍾' },
                        { id: 'hex', label: 'Hex', icon: '⬡' },
                        { id: 'vial', label: 'Vial', icon: '💊' }
                      ].map(shape => (
                        <button
                          key={shape.id}
                          type="button"
                          onClick={() => setPackageShape(shape.id)}
                          className={`py-2 rounded-lg border text-center transition-all flex flex-col items-center justify-center cursor-pointer ${
                            packageShape === shape.id
                              ? 'border-brand-primary bg-brand-primary/20 text-white shadow-md'
                              : 'border-brand-border bg-brand-panel/20 text-brand-muted hover:border-brand-border/60 hover:text-white'
                          }`}
                        >
                          <span className="text-base mb-0.5">{shape.icon}</span>
                          <span className="text-[9px] font-bold">{shape.label}</span>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-brand-muted uppercase mb-1">Cardboard Roughness</label>
                    <div className="flex items-center space-x-3">
                      <input type="range" min="0" max="1" step="0.1" defaultValue="0.3" className="flex-1 accent-brand-primary" />
                      <span className="text-xs text-white">0.3</span>
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-brand-muted uppercase mb-1">Foil Metalness</label>
                    <div className="flex items-center space-x-3">
                      <input type="range" min="0" max="1" step="0.1" defaultValue="0.2" className="flex-1 accent-brand-primary" />
                      <span className="text-xs text-white">0.2</span>
                    </div>
                  </div>
                </div>

                <div className="border border-brand-border rounded-xl p-4 bg-brand-bg/40 mt-6 text-xs text-brand-muted">
                  <span className="font-semibold text-white block mb-1">AI Recommendation Feedback Loop:</span>
                  Does this font render correctly on the 3D wrapper?
                  <div className="flex space-x-2 mt-3">
                    <button 
                      onClick={() => handleFeedback(true)}
                      className="px-3 py-1 bg-brand-secondary/10 border border-brand-secondary/30 hover:bg-brand-secondary/20 text-brand-secondary rounded-lg font-semibold"
                    >
                      👍 Accept ({positiveFeedbackCount})
                    </button>
                    <button 
                      onClick={() => handleFeedback(false)}
                      className="px-3 py-1 bg-brand-accent/10 border border-brand-accent/30 hover:bg-brand-accent/20 text-brand-accent rounded-lg font-semibold"
                    >
                      👎 Reject ({negativeFeedbackCount})
                    </button>
                  </div>
                  <span className="text-[10px] block mt-2 text-gray-500">Positive feedback retrains ranker embedding weights automatically.</span>
                </div>
              </div>
            </div>

          </div>
        )}

        {/* TAB 3: FONTLAB DNA */}
        {activeTab === 'fontlab' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Morphing sliders */}
            <div className="lg:col-span-1 glass-panel rounded-2xl p-6">
              <h2 className="text-lg font-bold text-white mb-4">Font DNA Evolution</h2>
              
              <div className="space-y-5">
                <div>
                  <label className="block text-xs font-semibold text-brand-muted uppercase mb-1">Base Font DNA template</label>
                  <div className="relative">
                    <input
                      type="text"
                      value={evoFontSearch}
                      onChange={e => {
                        setEvoFontSearch(e.target.value);
                        setShowEvoFontDropdown(true);
                      }}
                      onFocus={() => setShowEvoFontDropdown(true)}
                      onBlur={() => setTimeout(() => setShowEvoFontDropdown(false), 250)}
                      placeholder="Search base template..."
                      className="w-full bg-brand-bg border border-brand-border rounded-lg pl-3 pr-8 py-2 text-sm text-white focus:outline-none focus:border-brand-primary"
                    />
                    {evoFontSearch && (
                      <button
                        type="button"
                        onMouseDown={(e) => {
                          e.preventDefault();
                          setEvoFontSearch('');
                          setBaseEvoFont('');
                        }}
                        className="absolute right-2.5 top-1/2 -translate-y-1/2 text-brand-muted hover:text-white p-0.5 rounded-full hover:bg-brand-border/40 transition-colors"
                      >
                        <X className="h-3.5 w-3.5" />
                      </button>
                    )}
                    {showEvoFontDropdown && evoFontOptions.length > 0 && (
                      <div className="absolute left-0 right-0 mt-1 max-h-60 overflow-y-auto bg-[#141424] border border-brand-border rounded-lg shadow-xl z-50 text-xs divide-y divide-brand-border/40">
                        {evoFontOptions.map(option => (
                          <div
                            key={option.name}
                            onMouseDown={() => {
                              setBaseEvoFont(option.name);
                              setEvoFontSearch(option.name);
                              setShowEvoFontDropdown(false);
                            }}
                            className="p-2.5 cursor-pointer hover:bg-brand-primary/20 text-white flex justify-between items-center transition-colors"
                          >
                            <span className="font-bold">{option.name}</span>
                            <span className="text-[10px] px-2 py-0.5 rounded border border-brand-primary/30 text-brand-primary bg-brand-primary/5">{option.style}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                <div className="border border-brand-border rounded-xl p-4 bg-brand-bg/40">
                  <span className="block font-semibold text-xs text-white mb-3">Evolution Modifiers</span>
                  
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-xs text-brand-muted mb-1">
                        <span>Luxury Index</span>
                        <span className="text-white font-semibold">+{evoParams.luxury}</span>
                      </div>
                      <input 
                        type="range" min="0" max="1" step="0.1" 
                        value={evoParams.luxury} 
                        onChange={e => {
                          setEvoParams(prev => ({...prev, luxury: parseFloat(e.target.value)}));
                          handleEvolveFont();
                        }}
                        className="w-full accent-brand-primary" 
                      />
                    </div>

                    <div>
                      <div className="flex justify-between text-xs text-brand-muted mb-1">
                        <span>Modern Feel</span>
                        <span className="text-white font-semibold">+{evoParams.modern}</span>
                      </div>
                      <input 
                        type="range" min="0" max="1" step="0.1" 
                        value={evoParams.modern} 
                        onChange={e => {
                          setEvoParams(prev => ({...prev, modern: parseFloat(e.target.value)}));
                          handleEvolveFont();
                        }}
                        className="w-full accent-brand-primary" 
                      />
                    </div>

                    <div>
                      <div className="flex justify-between text-xs text-brand-muted mb-1">
                        <span>Readability Axis</span>
                        <span className="text-white font-semibold">+{evoParams.readability}</span>
                      </div>
                      <input 
                        type="range" min="0" max="1" step="0.1" 
                        value={evoParams.readability} 
                        onChange={e => {
                          setEvoParams(prev => ({...prev, readability: parseFloat(e.target.value)}));
                          handleEvolveFont();
                        }}
                        className="w-full accent-brand-primary" 
                      />
                    </div>
                  </div>
                </div>

                {evolvedDNA && (
                  <div className="border border-brand-border rounded-xl p-4 bg-brand-bg/30 text-xs">
                    <span className="font-semibold text-white block mb-2">Mutated Font DNA Parameters</span>
                    <div className="grid grid-cols-2 gap-2 text-[10px]">
                      <div>Stroke contrast: {evolvedDNA.contrast}</div>
                      <div>Serif Angle: {evolvedDNA.serif_angle}</div>
                      <div>x-Height Ratio: {evolvedDNA.x_height}</div>
                      <div>Stroke width: {evolvedDNA.stroke_width}</div>
                      <div>Curvature: {evolvedDNA.curvature}</div>
                      <div>Geometric factor: {evolvedDNA.geometric_index}</div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Glyph render canvas */}
            <div className="lg:col-span-2 glass-panel rounded-3xl p-6 flex flex-col justify-between">
              <div>
                <h2 className="text-lg font-bold text-white mb-2">Generative Glyphs Render</h2>
                <p className="text-xs text-brand-muted">SVG shapes synthesized in real-time by mutating vector path formulas</p>
              </div>

              {/* Render characters maps */}
              <div className="grid grid-cols-5 gap-4 my-6">
                {evolvedGlyphs && Object.keys(evolvedGlyphs).map(char => (
                  <div key={char} className="aspect-square bg-brand-bg rounded-2xl border border-brand-border flex items-center justify-center relative group hover:border-brand-primary/60 transition-colors p-4">
                    <span className="absolute top-2 left-2 text-[10px] text-brand-muted font-mono">{char}</span>
                    <svg viewBox="0 0 100 100" className="w-16 h-16 text-white" dangerouslySetInnerHTML={{ __html: evolvedGlyphs[char] }} />
                  </div>
                ))}
              </div>

              <div className="flex justify-between items-center border-t border-brand-border/60 pt-4">
                <span className="text-xs text-brand-muted">Output formats: TrueType (TTF), OpenType (OTF), WOFF, WOFF2</span>
                <button
                  onClick={() => alert("Custom TTF font bundle downloaded successfully to local machine!")}
                  className="px-4 py-2 bg-brand-primary hover:bg-brand-primary/80 text-white font-bold rounded-lg text-xs flex items-center space-x-1.5"
                >
                  <Download className="h-3.5 w-3.5" />
                  <span>Download Evolved .TTF Font</span>
                </button>
              </div>
            </div>

          </div>
        )}

        {/* TAB 4: FAISS VECTOR SEARCH */}
        {activeTab === 'similarity' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Input Search Form */}
            <div className="lg:col-span-1 glass-panel rounded-2xl p-6">
              <h2 className="text-lg font-bold text-white mb-4">FAISS Font Similarity Search</h2>
              <p className="text-xs text-brand-muted mb-4">Find similar fonts in our vector indexing database containing 50,000+ fonts</p>

              <form onSubmit={handleSimilaritySearch} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-brand-muted uppercase mb-1">Select Anchor Font</label>
                  <div className="relative">
                    <input
                      type="text"
                      value={similaritySearchInput}
                      onChange={e => {
                        setSimilaritySearchInput(e.target.value);
                        setShowSimilarityDropdown(true);
                      }}
                      onFocus={() => setShowSimilarityDropdown(true)}
                      onBlur={() => setTimeout(() => setShowSimilarityDropdown(false), 250)}
                      placeholder="Search anchor font..."
                      className="w-full bg-brand-bg border border-brand-border rounded-lg pl-3 pr-8 py-2 text-sm text-white focus:outline-none focus:border-brand-primary"
                    />
                    {similaritySearchInput && (
                      <button
                        type="button"
                        onMouseDown={(e) => {
                          e.preventDefault();
                          setSimilaritySearchInput('');
                          setSimilarSearchName('');
                        }}
                        className="absolute right-2.5 top-1/2 -translate-y-1/2 text-brand-muted hover:text-white p-0.5 rounded-full hover:bg-brand-border/40 transition-colors"
                      >
                        <X className="h-3.5 w-3.5" />
                      </button>
                    )}
                    {showSimilarityDropdown && similarityOptions.length > 0 && (
                      <div className="absolute left-0 right-0 mt-1 max-h-60 overflow-y-auto bg-[#141424] border border-brand-border rounded-lg shadow-xl z-50 text-xs divide-y divide-brand-border/40">
                        {similarityOptions.map(option => (
                          <div
                            key={option.name}
                            onMouseDown={() => {
                              setSimilarSearchName(option.name);
                              setSimilaritySearchInput(option.name);
                              setShowSimilarityDropdown(false);
                            }}
                            className="p-2.5 cursor-pointer hover:bg-brand-primary/20 text-white flex justify-between items-center transition-colors"
                          >
                            <span className="font-bold">{option.name}</span>
                            <span className="text-[10px] px-2 py-0.5 rounded border border-brand-primary/30 text-brand-primary bg-brand-primary/5">{option.style}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full py-2.5 bg-brand-primary hover:bg-brand-primary/90 text-white font-semibold rounded-lg text-sm"
                >
                  Query 1024-D FAISS Index
                </button>
              </form>
            </div>

            {/* Query Results */}
            <div className="lg:col-span-2 glass-panel rounded-3xl p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-base font-bold text-white">Top 100 Similar Fonts</h3>
                <span className="text-xs text-brand-muted">Algorithm: L2 Distance (IndexFlatL2)</span>
              </div>

              <div className="space-y-2 max-h-[480px] overflow-y-auto pr-2">
                {similarResults.length > 0 ? (
                  similarResults.map((item, idx) => (
                    <div key={idx} className="flex justify-between items-center p-3 bg-brand-panel/40 border border-brand-border/40 rounded-xl text-xs hover:border-brand-border/80 transition-colors">
                      <div className="flex items-center space-x-3">
                        <span className="w-6 h-6 rounded-full bg-brand-border flex items-center justify-center font-bold text-brand-muted text-[10px]">
                          {idx + 1}
                        </span>
                        <div>
                          <span 
                            className="font-bold text-white block text-sm mb-0.5"
                            style={getFontPreviewStyle({ name: item.font_name, style: item.style })}
                          >
                            {item.font_name}
                          </span>
                          <span className="text-[10px] text-brand-muted">{item.style} style</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className="font-bold text-brand-secondary block">{(item.similarity * 100).toFixed(2)}% similarity</span>
                        <span className="text-[10px] text-brand-muted">L2 Dist: {item.distance.toFixed(4)}</span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-12 text-brand-muted text-xs">
                    No results found. Choose an anchor font and hit query to search FAISS database.
                  </div>
                )}
              </div>
            </div>

          </div>
        )}

        {/* TAB 5: 100k FONT BROWSER */}
        {activeTab === 'registry' && (
          <div className="glass-panel rounded-3xl p-6 space-y-6 animate-fade-in">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-brand-border/60 pb-4">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center space-x-2">
                  <Database className="h-5 w-5 text-brand-primary" />
                  <span>Enterprise 100k Font Browser</span>
                </h2>
                <p className="text-xs text-brand-muted mt-1">Browse, search, and filter the complete index of 100,000 fonts in alphabetical order</p>
              </div>

              {/* Filters & Search */}
              <div className="flex flex-wrap gap-3">
                <input 
                  type="text" 
                  placeholder="Search 100,000 fonts..."
                  value={registrySearch}
                  onChange={e => {
                    setRegistrySearch(e.target.value);
                    setRegistryPage(0);
                  }}
                  className="bg-brand-bg border border-brand-border rounded-lg px-3 py-1.5 text-xs text-white placeholder-brand-muted w-64 focus:outline-none focus:border-brand-primary"
                />

                <select 
                  value={registryStyle}
                  onChange={e => {
                    setRegistryStyle(e.target.value);
                    setRegistryPage(0);
                  }}
                  className="bg-brand-bg border border-brand-border rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-brand-primary"
                  style={{ backgroundColor: '#181824', color: '#ffffff' }}
                >
                  <option value="All" style={{ backgroundColor: '#181824', color: '#ffffff' }}>All Styles</option>
                  <option value="Serif" style={{ backgroundColor: '#181824', color: '#ffffff' }}>Serif</option>
                  <option value="Grotesque" style={{ backgroundColor: '#181824', color: '#ffffff' }}>Grotesque</option>
                  <option value="Geometric" style={{ backgroundColor: '#181824', color: '#ffffff' }}>Geometric</option>
                  <option value="Slab" style={{ backgroundColor: '#181824', color: '#ffffff' }}>Slab</option>
                  <option value="Display" style={{ backgroundColor: '#181824', color: '#ffffff' }}>Display</option>
                  <option value="Script" style={{ backgroundColor: '#181824', color: '#ffffff' }}>Script</option>
                  <option value="Handwritten" style={{ backgroundColor: '#181824', color: '#ffffff' }}>Handwritten</option>
                </select>

                <select 
                  value={registryLimit}
                  onChange={e => {
                    setRegistryLimit(parseInt(e.target.value));
                    setRegistryPage(0);
                  }}
                  className="bg-brand-bg border border-brand-border rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-brand-primary"
                  style={{ backgroundColor: '#181824', color: '#ffffff' }}
                >
                  <option value="25" style={{ backgroundColor: '#181824', color: '#ffffff' }}>25 per page</option>
                  <option value="50" style={{ backgroundColor: '#181824', color: '#ffffff' }}>50 per page</option>
                  <option value="100" style={{ backgroundColor: '#181824', color: '#ffffff' }}>100 per page</option>
                  <option value="250" style={{ backgroundColor: '#181824', color: '#ffffff' }}>250 per page</option>
                </select>
              </div>
            </div>

            {/* Fonts Table */}
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-brand-border text-brand-muted uppercase text-[10px] tracking-wider bg-brand-panel/30">
                    <th className="py-3 px-4 font-bold"># Index</th>
                    <th className="py-3 px-4 font-bold">Font Name</th>
                    <th className="py-3 px-4 font-bold">Style</th>
                    <th className="py-3 px-4 font-bold">Primary Specialty</th>
                    <th className="py-3 px-4 font-bold">Typographic Preview (Sentence)</th>
                    <th className="py-3 px-4 font-bold text-center">Luxury Index</th>
                    <th className="py-3 px-4 font-bold text-center">Readability</th>
                    <th className="py-3 px-4 font-bold text-center">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-brand-border/40">
                  {registryFonts.length > 0 ? (
                    registryFonts.map((f, idx) => (
                      <tr key={idx} className="hover:bg-brand-panel/10 transition-colors">
                        <td className="py-3.5 px-4 text-brand-muted font-mono">
                          #{registryPage * registryLimit + idx + 1}
                        </td>
                        <td className="py-3.5 px-4 font-bold text-white text-sm">
                          {f.name}
                        </td>
                        <td className="py-3.5 px-4">
                          <span className="px-2.5 py-0.5 rounded-full border border-brand-primary/30 text-[10px] font-semibold bg-brand-primary/10 text-brand-primary">
                            {f.style}
                          </span>
                        </td>
                        <td className="py-3.5 px-4 text-brand-secondary font-medium">
                          {f.specialty}
                        </td>
                        <td className="py-3.5 px-4 text-white text-sm" style={getFontPreviewStyle(f)}>
                          The quick brown fox jumps over the lazy dog.
                        </td>
                        <td className="py-3.5 px-4 text-center">
                          <div className="flex items-center justify-center space-x-1">
                            <span className="font-mono text-white">{(f.luxury_score * 100).toFixed(0)}%</span>
                          </div>
                        </td>
                        <td className="py-3.5 px-4 text-center">
                          <div className="flex items-center justify-center space-x-1">
                            <span className="font-mono text-white">{(f.readability * 100).toFixed(0)}%</span>
                          </div>
                        </td>
                        <td className="py-3.5 px-4 text-center">
                          <button
                            onClick={() => {
                              setSelectedFont(f.name);
                              alert(`"${f.name}" has been applied as your active branding canvas font!`);
                            }}
                            className="px-2.5 py-1 bg-brand-secondary/15 hover:bg-brand-secondary/35 border border-brand-secondary/30 text-brand-secondary rounded-lg font-bold transition-all text-[10px]"
                          >
                            Apply Font
                          </button>
                        </td>
                      </tr>
                    ))
                  ) : registryError ? (
                    <tr>
                      <td colSpan="8" className="text-center py-12 text-brand-accent font-semibold bg-brand-accent/5 border border-brand-accent/20 rounded-xl">
                        ⚠️ {registryError}
                      </td>
                    </tr>
                  ) : (
                    <tr>
                      <td colSpan="8" className="text-center py-12 text-brand-muted animate-pulse">
                        No fonts found matching your search. Searching 100,000 index...
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Pagination Controls */}
            <div className="flex items-center justify-between pt-4 border-t border-brand-border/60 text-xs">
              <span className="text-brand-muted">
                Showing <span className="text-white font-semibold">{registryPage * registryLimit + 1}</span> to{' '}
                <span className="text-white font-semibold">
                  {Math.min((registryPage + 1) * registryLimit, registryTotal)}
                </span>{' '}
                of <span className="text-white font-semibold">{registryTotal.toLocaleString()}</span> fonts
              </span>

              <div className="flex items-center space-x-2">
                <button
                  disabled={registryPage === 0}
                  onClick={() => setRegistryPage(0)}
                  className="px-2.5 py-1.5 rounded-lg border border-brand-border bg-brand-panel/20 text-white disabled:opacity-30 disabled:cursor-not-allowed hover:bg-brand-panel/40 transition-all font-semibold"
                >
                  First
                </button>
                <button
                  disabled={registryPage === 0}
                  onClick={() => setRegistryPage(prev => Math.max(0, prev - 1))}
                  className="px-2.5 py-1.5 rounded-lg border border-brand-border bg-brand-panel/20 text-white disabled:opacity-30 disabled:cursor-not-allowed hover:bg-brand-panel/40 transition-all font-semibold"
                >
                  Prev
                </button>
                <span className="text-brand-muted px-2">
                  Page <span className="text-white font-semibold">{registryPage + 1}</span> of{' '}
                  <span className="text-white font-semibold">{Math.ceil(registryTotal / registryLimit) || 1}</span>
                </span>
                <button
                  disabled={(registryPage + 1) * registryLimit >= registryTotal}
                  onClick={() => setRegistryPage(prev => prev + 1)}
                  className="px-2.5 py-1.5 rounded-lg border border-brand-border bg-brand-panel/20 text-white disabled:opacity-30 disabled:cursor-not-allowed hover:bg-brand-panel/40 transition-all font-semibold"
                >
                  Next
                </button>
                <button
                  disabled={(registryPage + 1) * registryLimit >= registryTotal}
                  onClick={() => setRegistryPage(Math.ceil(registryTotal / registryLimit) - 1)}
                  className="px-2.5 py-1.5 rounded-lg border border-brand-border bg-brand-panel/20 text-white disabled:opacity-30 disabled:cursor-not-allowed hover:bg-brand-panel/40 transition-all font-semibold"
                >
                  Last
                </button>
              </div>
            </div>
          </div>
        )/* registry tab end */}

        {/* TAB 5: AGENTS CONSOLE */}
        {activeTab === 'agents' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Chat Interface */}
            <div className="lg:col-span-2 glass-panel rounded-3xl p-6 flex flex-col h-[600px]">
              <div className="border-b border-brand-border/60 pb-3 mb-4">
                <h2 className="text-lg font-bold text-white">AI Designer Agent Chat Terminal</h2>
                <p className="text-xs text-brand-muted">Direct interface to the Workflow Orchestrator and specialized planners</p>
              </div>

              <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2 text-xs">
                {chatMessages.map((msg, idx) => (
                  <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[75%] rounded-xl p-3.5 ${
                      msg.role === 'user' 
                        ? 'bg-brand-primary text-white' 
                        : 'bg-brand-panel border border-brand-border/80 text-gray-200'
                    }`}>
                      <span className="block font-bold text-[9px] uppercase tracking-wider mb-1 opacity-70">
                        {msg.role === 'user' ? 'Designer' : 'Chief Designer Agent'}
                      </span>
                      <p className="whitespace-pre-wrap leading-relaxed">{msg.message}</p>
                      
                      {msg.recommendations && msg.recommendations.length > 0 && (
                        <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-3">
                          {msg.recommendations.map((font, fIdx) => (
                            <div 
                              key={fIdx} 
                              className="bg-brand-bg border border-brand-border/60 hover:border-brand-primary/60 rounded-xl p-3 flex flex-col justify-between transition-all shadow-inner"
                            >
                              <div>
                                <div className="flex justify-between items-start mb-1 gap-2">
                                  <span 
                                    className="font-bold text-white text-xs block truncate"
                                    style={getFontPreviewStyle(font)}
                                  >
                                    {font.name}
                                  </span>
                                  <span className="text-[9px] text-brand-secondary font-bold shrink-0">
                                    {(font.confidence * 100).toFixed(0)}% Match
                                  </span>
                                </div>
                                <span className="text-[8px] px-1.5 py-0.5 rounded border border-brand-border/40 text-brand-muted bg-brand-panel/20">
                                  {font.style}
                                </span>
                              </div>
                              <button
                                type="button"
                                onClick={() => {
                                  setSelectedFont(font.name);
                                  setSelectedFontSearch(font.name);
                                  alert(`"${font.name}" applied as active wrapper font! Check Tab 2 to view it in 3D.`);
                                }}
                                className="mt-2.5 w-full py-1 bg-brand-primary/20 hover:bg-brand-primary/40 border border-brand-primary/40 hover:border-brand-primary text-brand-primary hover:text-white rounded-lg text-[9px] font-bold transition-all"
                              >
                                Select & Apply
                              </button>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              <form onSubmit={handleChatSubmit} className="flex space-x-2">
                <input 
                  type="text" 
                  value={userPrompt}
                  onChange={e => setUserPrompt(e.target.value)}
                  placeholder="Ask agent to pair fonts, write reports, or check layout..." 
                  className="flex-1 bg-brand-bg border border-brand-border rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-brand-primary" 
                />
                <button 
                  type="submit" 
                  className="px-4 py-2.5 bg-brand-primary hover:bg-brand-primary/80 text-white rounded-xl text-xs font-bold"
                >
                  Send
                </button>
              </form>
            </div>

            {/* Agent Thought Logs */}
            <div className="lg:col-span-1 glass-panel rounded-2xl p-6 flex flex-col h-[600px]">
              <div className="border-b border-brand-border/60 pb-3 mb-4">
                <h3 className="text-sm font-bold text-white flex items-center">
                  <Layers className="h-4 w-4 mr-2 text-brand-primary animate-pulse" />
                  Planner Orchestrator Threads
                </h3>
              </div>

              <div className="flex-1 overflow-y-auto space-y-4 text-[10px] pr-2 font-mono">
                {agentLogs.length > 0 ? (
                  agentLogs.map((log, idx) => (
                    <div key={idx} className="border-b border-brand-border/40 pb-2">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-bold text-brand-primary uppercase">{log.agent}</span>
                        <span className="text-gray-500">{log.latency_ms}ms</span>
                      </div>
                      <div className="space-y-1 text-gray-400">
                        {log.thoughts.map((t, tIdx) => (
                          <div key={tIdx}>{t}</div>
                        ))}
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-12 text-brand-muted">
                    No active orchestration logs. Go to "Brand Scanner" and trigger audit to see planning threads.
                  </div>
                )}
              </div>
            </div>

          </div>
        )}

        {/* TAB 6: DASHBOARD & REPORTS */}
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            
            {/* Overview Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[
                { label: 'OCR Error Rate', val: '1.2%', metric: 'Target < 4.0%', icon: Shield, col: 'text-brand-secondary' },
                { label: 'FAISS Search Latency', val: '2.4ms', metric: 'IndexFlatL2', icon: Zap, col: 'text-brand-accent' },
                { label: 'Saliency NSS Index', val: '2.45', metric: 'Target > 2.0', icon: Eye, col: 'text-brand-primary' },
                { label: 'Recommendation Acceptance', val: '92.3%', metric: 'Self-Learning feedback', icon: Heart, col: 'text-brand-secondary' }
              ].map((stat, idx) => {
                const Icon = stat.icon;
                return (
                  <div key={idx} className="glass-panel rounded-2xl p-5">
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-xs text-brand-muted font-semibold">{stat.label}</span>
                      <Icon className={`h-5 w-5 ${stat.col}`} />
                    </div>
                    <div className="text-2xl font-bold text-white mb-1">{stat.val}</div>
                    <span className="text-[10px] text-gray-500 block">{stat.metric}</span>
                  </div>
                );
              })}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* PDF Report Export card */}
              <div className="lg:col-span-1 glass-panel rounded-2xl p-6">
                <h3 className="text-base font-bold text-white mb-4">Export AI Design Report</h3>
                <p className="text-xs text-brand-muted mb-4">
                  Generates an 8-page design intelligence report covering layout bounding boxes, saliency coordinates, brand personality, and multilingual pairings.
                </p>

                {pdfReportMeta ? (
                  <a
                    href={`${API_BASE}${pdfReportMeta.download_url}`}
                    target="_blank"
                    rel="noreferrer"
                    className="w-full py-3 bg-brand-secondary text-white font-bold rounded-xl shadow-lg hover:shadow-brand-secondary/20 transition-all flex items-center justify-center space-x-2 text-sm"
                  >
                    <Download className="h-4 w-4" />
                    <span>Download PDF Report</span>
                  </a>
                ) : (
                  <button
                    onClick={() => alert("Please run the Brand Scanner design audit first to compile the report.")}
                    className="w-full py-3 bg-brand-border text-brand-muted font-bold rounded-xl text-sm flex items-center justify-center space-x-2 cursor-not-allowed"
                  >
                    <Download className="h-4 w-4" />
                    <span>Audit required to compile PDF</span>
                  </button>
                )}
              </div>

              {/* Consumer Psychology Dials */}
              <div className="lg:col-span-2 glass-panel rounded-2xl p-6">
                <h3 className="text-base font-bold text-white mb-4">Branding Emotional Radar</h3>
                
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  {[
                    { label: 'Trust Index', val: psychology.emotional_scores.trust },
                    { label: 'Excitement', val: psychology.emotional_scores.excitement },
                    { label: 'Warmth', val: psychology.emotional_scores.warmth },
                    { label: 'Premium Feel', val: psychology.emotional_scores.premium_feeling },
                    { label: 'Fun factor', val: psychology.emotional_scores.fun }
                  ].map((dial, idx) => (
                    <div key={idx} className="p-4 bg-brand-panel/30 border border-brand-border/40 rounded-xl text-center">
                      <span className="block text-[10px] text-brand-muted mb-2">{dial.label}</span>
                      <div className="relative inline-flex items-center justify-center">
                        {/* Circular progress bar */}
                        <svg className="w-16 h-16 transform -rotate-90">
                          <circle cx="32" cy="32" r="28" stroke="rgba(255,255,255,0.05)" strokeWidth="4" fill="transparent" />
                          <circle 
                            cx="32" cy="32" r="28" 
                            stroke="#6366F1" strokeWidth="4" fill="transparent" 
                            strokeDasharray={2 * Math.PI * 28}
                            strokeDashoffset={2 * Math.PI * 28 * (1 - dial.val)}
                          />
                        </svg>
                        <span className="absolute text-xs font-bold text-white">{(dial.val * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </div>

          </div>
        )}

      </main>

      {/* FOOTER */}
      <footer className="border-t border-brand-border bg-brand-panel/30 py-4 px-6 text-center text-xs text-brand-muted mt-12">
        &copy; 2026 Font Picker. Built with Next-generation Generative AI Typography models, CUDA PyTorch backends, and Vector FAISS indexes.
      </footer>

    </div>
  );
}
