<<<<<<< HEAD
opend)# SalonGenZ UI Design System
=======
# SalonGenZ UI Design System
>>>>>>> 6866a0ca7ed0af784d176d8ecdcf32bd4a982581
*Based on Time Sync⚡ AI Scheduler - Elite GenZ Design*

## 🎨 Design Philosophy

### Core Principles
- **Mobile-First**: All components designed for mobile, enhanced for desktop
- **GenZ Optimized**: Modern, clean, with subtle animations and gradients
- **Kenya-First**: Culturally relevant with local context
- **Elite Experience**: Premium feel with attention to detail

### Color Palette

#### Primary Colors
```css
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--secondary-gradient: linear-gradient(135deg, #ffd700 0%, #ffb347 50%, #ff8c00 100%);
--success-gradient: linear-gradient(135deg, #28a745 0%, #20c997 100%);
--charcoal-text: #36454f;
--soft-text: #6c757d;
```

#### Background Colors
```css
--bg-primary: #ffffff;
--bg-secondary: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
--bg-card: rgba(255, 255, 255, 0.95);
--bg-overlay: rgba(102, 126, 234, 0.05);
```

## 🧩 Component Standards

### 1. Headers & Titles
```css
.section-title {
  color: #36454f !important; /* Charcoal grey for visibility */
  font-weight: 600;
  font-size: 1.2rem;
  margin: 0 0 0.5rem 0;
}

.section-subtitle {
  color: #36454f !important;
  opacity: 0.8;
  font-size: 0.9rem;
  margin: 0;
}
```

### 2. Cards & Containers
```css
.elite-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border: 1px solid #dee2e6;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.elite-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}
```

### 3. Buttons
```css
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-elite {
  background: linear-gradient(135deg, #ffd700 0%, #ffb347 50%, #ff8c00 100%);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}
```

### 4. Form Inputs
```css
.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  font-size: 0.9rem;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  transition: all 0.3s ease;
  font-weight: 500;
  color: #2c3e50;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1), 0 4px 12px rgba(102, 126, 234, 0.2);
  transform: translateY(-1px);
}
```

### 5. Pagination
```css
.pagination-container {
  margin-top: 1.5rem;
  text-align: center;
}

.pagination-info {
  color: #6c757d;
  font-size: 0.8rem;
  margin-bottom: 1rem;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.pagination-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: #5a6fd8;
  transform: translateY(-1px);
}
```

## 📱 Responsive Design

### Breakpoints
```css
/* Mobile First */
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
```

### Grid Systems
```css
/* Mobile: 1 column, Tablet: 2 columns, Desktop: 3-4 columns */
.responsive-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .responsive-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {
  .responsive-grid { grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
}
```

## 🎭 Animations

### Standard Transitions
```css
.smooth-transition {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-lift:hover {
  transform: translateY(-2px);
}

.focus-glow:focus {
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
```

### Loading States
```css
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-top: 2px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

## 🏷️ Component Classes

### Layout Classes
- `.elite-container` - Main container with max-width and centering
- `.elite-section` - Section wrapper with proper spacing
- `.elite-grid` - Responsive grid layout
- `.elite-flex` - Flexible layout with gap

### State Classes
- `.active` - Active state for interactive elements
- `.selected` - Selected state for choices
- `.disabled` - Disabled state styling
- `.loading` - Loading state with spinner

### Utility Classes
- `.text-charcoal` - Charcoal grey text color
- `.text-soft` - Soft grey text color
- `.bg-gradient` - Primary gradient background
- `.shadow-soft` - Soft shadow effect
- `.rounded-lg` - Large border radius (12px)
- `.rounded-xl` - Extra large border radius (16px)

## 🎯 AI Integration Standards

### Context Patterns
```javascript
// Standard aihandle context structure
const aiContext = {
  aihandle_prefix: 'aihandle_[feature_name]',
  aihandle_context_type: '[specific_context]',
  aihandle_locale: 'kenya_east_africa_genz',
  // ... specific context data
};
```

### Common Prefixes
- `aihandle_timesync_scheduler` - Time scheduling
- `aihandle_salon_matchmaker` - Salon matching
- `aihandle_smart_notifications` - Notification system
- `aihandle_customer_insights` - Customer analytics

This design system ensures consistency across all SalonGenZ applications while maintaining the elite, GenZ-optimized experience that users expect.
