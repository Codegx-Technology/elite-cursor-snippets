'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Card from './Card';
import LoadingStates from '@/components/ui/LoadingStates';
import ErrorStates from '@/components/ui/ErrorStates';
import {
  FaVideo,
  FaImages,
  FaMusic,
  FaFlag,
  FaMountain,
  FaGlobe,
  FaPlay,
  FaArrowRight,
  FaStar,
  FaUsers,
  FaChartLine
} from 'react-icons/fa';

// [SNIPPET]: thinkwithai + kenyafirst + refactorclean
// [CONTEXT]: Enterprise welcome page with Kenya-first design and cultural authenticity
// [GOAL]: Create engaging landing experience showcasing platform capabilities
// [TASK]: Implement welcome page with cultural elements, feature highlights, and clear CTAs

export default function Welcome({ title }: { title: string }) {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [stats, setStats] = useState({
    videosGenerated: 0,
    happyCreators: 0,
    countriesServed: 0
  });

  useEffect(() => {
    // Check authentication status
    const token = localStorage.getItem('jwt_token');
    setIsLoggedIn(!!token);
  }, []);

  // Kenya-first showcase slides
  const showcaseSlides = [
    {
      title: "Mount Kenya Adventure",
      description: "Cinematic journey through Kenya&apos;s highest peak",
      thumbnail: "🏔️",
      category: "Tourism"
    },
    {
      title: "Nairobi Tech Innovation",
      description: "Silicon Savannah startup success story",
      thumbnail: "💻",
      category: "Technology"
    },
    {
      title: "Coastal Beauty",
      description: "Diani Beach paradise showcase",
      thumbnail: "🏖️",
      category: "Travel"
    },
    {
      title: "Wildlife Safari",
      description: "Maasai Mara Big Five experience",
      thumbnail: "🦁",
      category: "Nature"
    }
  ];

  // Animate stats on load
  useEffect(() => {
    const animateStats = () => {
      const targets = { videosGenerated: 2847, happyCreators: 1250, countriesServed: 15 };
      const duration = 2000;
      const steps = 60;
      const stepDuration = duration / steps;

      let step = 0;
      const timer = setInterval(() => {
        step++;
        const progress = step / steps;

        setStats({
          videosGenerated: Math.floor(targets.videosGenerated * progress),
          happyCreators: Math.floor(targets.happyCreators * progress),
          countriesServed: Math.floor(targets.countriesServed * progress)
        });

        if (step >= steps) {
          clearInterval(timer);
          setStats(targets);
        }
      }, stepDuration);
    };

    animateStats();
  }, []);

  // Auto-rotate showcase slides
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % showcaseSlides.length);
    }, 4000);

    return () => clearInterval(timer);
  }, [showcaseSlides.length]);

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl">
        <div
          className="p-12 text-white text-center"
          style={{
            background: 'linear-gradient(135deg, #00A651 0%, #FF6B35 50%, #FFD700 100%)'
          }}
        >
          <div className="flex justify-center items-center mb-6">
            <div className="relative">
              <svg width="80" height="54" viewBox="0 0 80 54" className="shadow-lg rounded animate-pulse">
                <defs>
                  <clipPath id="waveClip">
                    <path d="M0,0 Q20,3 40,0 T80,0 L80,54 Q60,51 40,54 T0,54 Z">
                      <animateTransform
                        attributeName="transform"
                        type="translate"
                        values="0,0; 2,1; 0,0; -2,-1; 0,0"
                        dur="3s"
                        repeatCount="indefinite"
                      />
                    </path>
                  </clipPath>
                </defs>
                
                <g clipPath="url(#waveClip)">
                  {/* Black stripe */}
                  <rect x="0" y="0" width="80" height="13.5" fill="#000000">
                    <animateTransform
                      attributeName="transform"
                      type="skewX"
                      values="0; 2; 0; -2; 0"
                      dur="2.5s"
                      repeatCount="indefinite"
                    />
                  </rect>
                  {/* Red stripe */}
                  <rect x="0" y="13.5" width="80" height="13.5" fill="#CE1126">
                    <animateTransform
                      attributeName="transform"
                      type="skewX"
                      values="0; -1.5; 0; 1.5; 0"
                      dur="2.8s"
                      repeatCount="indefinite"
                    />
                  </rect>
                  {/* Green stripe */}
                  <rect x="0" y="27" width="80" height="13.5" fill="#007A3D">
                    <animateTransform
                      attributeName="transform"
                      type="skewX"
                      values="0; 1; 0; -1; 0"
                      dur="3.2s"
                      repeatCount="indefinite"
                    />
                  </rect>
                  {/* White stripes */}
                  <rect x="0" y="10.8" width="80" height="2.7" fill="#FFFFFF"/>
                  <rect x="0" y="24.3" width="80" height="2.7" fill="#FFFFFF"/>
                  <rect x="0" y="37.8" width="80" height="2.7" fill="#FFFFFF"/>
                  
                  {/* Shield and spears */}
                  <g transform="translate(40, 27)">
                    <g>
                      <animateTransform
                        attributeName="transform"
                        type="translate"
                        values="0,0; 1,0.5; 0,0; -0.5,-0.3; 0,0"
                        dur="2.7s"
                        repeatCount="indefinite"
                      />
                      {/* Traditional Maasai shield */}
                      <ellipse cx="0" cy="0" rx="8" ry="12" fill="#8B4513" stroke="#000" strokeWidth="0.5"/>
                      <ellipse cx="0" cy="0" rx="6" ry="10" fill="#FFFFFF"/>
                      <ellipse cx="0" cy="0" rx="4" ry="8" fill="#CE1126"/>
                      {/* Crossed spears */}
                      <line x1="-12" y1="-8" x2="12" y2="8" stroke="#8B4513" strokeWidth="1.5"/>
                      <line x1="12" y1="-8" x2="-12" y2="8" stroke="#8B4513" strokeWidth="1.5"/>
                      {/* Spear tips */}
                      <polygon points="-12,-8 -10,-6 -14,-6" fill="#C0C0C0"/>
                      <polygon points="12,8 10,6 14,6" fill="#C0C0C0"/>
                      <polygon points="12,-8 10,-6 14,-6" fill="#C0C0C0"/>
                      <polygon points="-12,8 -10,6 -14,6" fill="#C0C0C0"/>
                    </g>
                  </g>
                </g>
              </svg>
            </div>
          </div>

          <h1 className="text-5xl font-bold mb-4">
            {title} 🇰🇪
          </h1>
          <p className="text-xl mb-2 text-green-100">
            Kenya&apos;s Premier AI-Powered Video Generation Platform
          </p>
          <p className="text-lg mb-8 text-yellow-100">
            Empowering African storytellers with cutting-edge AI technology
          </p>

          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6">
            {isLoggedIn ? (
              <>
                <Link href="/video-generate" className="hover:no-underline">
                  <button className="bg-white text-green-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition-all duration-300 flex items-center space-x-2 shadow-lg">
                    <FaPlay />
                    <span>Start Creating</span>
                    <FaArrowRight />
                  </button>
                </Link>
                <Link href="/dashboard" className="hover:no-underline">
                  <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-white hover:text-green-600 transition-all duration-300 flex items-center space-x-2">
                    <FaChartLine />
                    <span>View Dashboard</span>
                  </button>
                </Link>
              </>
            ) : (
              <>
                <Link href="/login" className="hover:no-underline">
                  <button className="bg-white text-green-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition-all duration-300 flex items-center space-x-2 shadow-lg">
                    <FaPlay />
                    <span>Get Started</span>
                    <FaArrowRight />
                  </button>
                </Link>
                <Link href="/demo" className="hover:no-underline">
                  <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-white hover:text-green-600 transition-all duration-300 flex items-center space-x-2">
                    <FaVideo />
                    <span>View Demo</span>
                  </button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="text-center p-6 hover-lift">
          <div className="text-3xl font-bold text-green-600 mb-2">{stats.videosGenerated.toLocaleString()}</div>
          <div className="text-gray-600">Videos Generated</div>
          <FaVideo className="mx-auto mt-2 text-green-600" size={24} />
        </Card>
        <Card className="text-center p-6 hover-lift">
          <div className="text-3xl font-bold text-blue-600 mb-2">{stats.happyCreators.toLocaleString()}</div>
          <div className="text-gray-600">Happy Creators</div>
          <FaUsers className="mx-auto mt-2 text-blue-600" size={24} />
        </Card>
        <Card className="text-center p-6 hover-lift">
          <div className="text-3xl font-bold text-orange-600 mb-2">{stats.countriesServed}</div>
          <div className="text-gray-600">Countries Served</div>
          <FaGlobe className="mx-auto mt-2 text-orange-600" size={24} />
        </Card>
      </div>

      {/* Feature Highlights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Features */}
        <Card className="p-8">
          <h2 className="section-title text-2xl mb-6">Platform Features</h2>
          <div className="space-y-6">
            <div className="flex items-start space-x-4">
              <div className="bg-blue-100 p-3 rounded-lg">
                <FaVideo className="text-blue-600" size={24} />
              </div>
              <div>
                <h3 className="font-semibold text-lg mb-2">AI Video Generation</h3>
                <p className="text-gray-600">Create stunning videos with Kenya-first cultural authenticity using advanced AI models.</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-green-100 p-3 rounded-lg">
                <FaImages className="text-green-600" size={24} />
              </div>
              <div>
                <h3 className="font-semibold text-lg mb-2">Cultural Image Generation</h3>
                <p className="text-gray-600">Generate beautiful, culturally relevant imagery showcasing African heritage and landscapes.</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-purple-100 p-3 rounded-lg">
                <FaMusic className="text-purple-600" size={24} />
              </div>
              <div>
                <h3 className="font-semibold text-lg mb-2">Swahili Voice Synthesis</h3>
                <p className="text-gray-600">Natural-sounding Kenyan voices with Swahili, English, and Sheng language support.</p>
              </div>
            </div>
          </div>
        </Card>

        {/* Showcase */}
        <Card className="p-8">
          <h2 className="section-title text-2xl mb-6">Recent Creations</h2>
          <div className="relative">
            <div className="bg-gray-100 rounded-lg p-8 text-center">
              <div className="text-6xl mb-4">{showcaseSlides[currentSlide].thumbnail}</div>
              <h3 className="font-bold text-xl mb-2">{showcaseSlides[currentSlide].title}</h3>
              <p className="text-gray-600 mb-4">{showcaseSlides[currentSlide].description}</p>
              <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                {showcaseSlides[currentSlide].category}
              </span>
            </div>

            {/* Slide indicators */}
            <div className="flex justify-center space-x-2 mt-4">
              {showcaseSlides.map((_, index) => (
                <button
                  key={index}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === currentSlide ? 'bg-blue-600' : 'bg-gray-300'
                  }`}
                  onClick={() => setCurrentSlide(index)}
                />
              ))}
            </div>
          </div>
        </Card>
      </div>

      {/* Cultural Footer */}
      <Card className="p-8 text-center">
        <div className="flex justify-center items-center space-x-2 mb-4">
          <span className="text-lg font-medium uppercase tracking-wide">MADE WITH IN KENYA</span>
        </div>
        <p className="text-gray-600 mb-6">
          Join thousands of African creators telling their stories with authentic, AI-powered content generation.
        </p>
        <div className="flex justify-center items-center space-x-6 text-sm text-gray-500">
          <div className="flex items-center space-x-1">
            <FaStar className="text-yellow-500" />
            <span>4.9/5 Rating</span>
          </div>
          <div>•</div>
          <div>Trusted by 1,250+ creators</div>
          <div>•</div>
          <div>Available in 15 countries</div>
        </div>
      </Card>
    </div>
  );
}
