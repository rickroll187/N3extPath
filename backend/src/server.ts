// File: backend/src/server.ts
/**
 * ⚙️🎸 N3EXTPATH - LEGENDARY BACKEND SERVER 🎸⚙️
 * Swiss precision Node.js/Express server with infinite code bro energy
 * Built: 2025-08-06 16:18:30 UTC by RICKROLL187
 * Email: letstalktech010@gmail.com
 * WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
 */

import 'express-async-errors';
import express, { Application, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import compression from 'compression';
import rateLimit from 'express-rate-limit';
import { createServer } from 'http';
import { Server as SocketIOServer } from 'socket.io';
import dotenv from 'dotenv';
import path from 'path';

// Internal imports
import { logger } from './utils/logger';
import { connectDatabase } from './database/connection';
import { errorHandler, notFoundHandler } from './middleware/errorHandler';
import { requestLogger } from './middleware/requestLogger';
import { founderAuth } from './middleware/founderAuth';
import { swissPrecisionValidator } from './middleware/validation';

// Routes
import authRoutes from './routes/auth';
import userRoutes from './routes/users';
import performanceRoutes from './routes/performance';
import okrRoutes from './routes/okrs';
import teamsRoutes from './routes/teams';
import notificationsRoutes from './routes/notifications';
import founderRoutes from './routes/founder';
import analyticsRoutes from './routes/analytics';

// Services
import { WebSocketService } from './services/websocketService';
import { RedisService } from './services/redisService';
import { EmailService } from './services/emailService';

// Load environment variables
dotenv.config();

// =====================================
// ⚙️ LEGENDARY SERVER CLASS ⚙️
// =====================================

class LegendaryServer {
  public app: Application;
  public server: any;
  public io: SocketIOServer;
  private port: number;
  private isFounderMode: boolean = false;

  constructor() {
    console.log('⚙️🎸⚙️ N3EXTPATH LEGENDARY BACKEND SERVER INITIALIZING! ⚙️🎸⚙️');
    console.log('Built with Swiss precision by RICKROLL187!');
    console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
    console.log(`🌅 Server initializing at: 2025-08-06 16:18:30 UTC`);
    console.log('🚀 LEGENDARY AFTERNOON SERVER ENERGY AT 16:18:30!');

    this.app = express();
    this.port = parseInt(process.env.PORT || '8080', 10);
    
    // Check if this is founder mode
    this.isFounderMode = process.env.FOUNDER_MODE === 'true' || 
                        process.env.NODE_ENV === 'founder' ||
                        process.env.RICKROLL187_FOUNDER === 'true';

    if (this.isFounderMode) {
      console.log('👑🎸👑 RICKROLL187 FOUNDER SERVER MODE ACTIVATED! 👑🎸👑');
      console.log('🚀 LEGENDARY FOUNDER SERVER WITH INFINITE CODE BRO ENERGY!');
      console.log('⚙️ SWISS PRECISION FOUNDER SERVER SYSTEM!');
      console.log('🌅 AFTERNOON FOUNDER SERVER POWER AT 16:18:30!');
    }

    this.initializeMiddleware();
    this.initializeRoutes();
    this.initializeErrorHandling();
    this.initializeSocket();
  }

  // =====================================
  // 🎸 MIDDLEWARE INITIALIZATION 🎸
  // =====================================

  private initializeMiddleware(): void {
    console.log('🔧 Initializing legendary middleware...');

    // Basic security and parsing
    this.app.use(helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          scriptSrc: ["'self'"],
          imgSrc: ["'self'", "data:", "https:"],
        },
      },
      crossOriginEmbedderPolicy: false,
    }));

    // CORS configuration
    this.app.use(cors({
      origin: process.env.FRONTEND_URL || 'http://localhost:3000',
      credentials: true,
      optionsSuccessStatus: 200,
      methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
      allowedHeaders: [
        'Origin', 
        'X-Requested-With', 
        'Content-Type', 
        'Accept', 
        'Authorization',
        'X-Founder-Request',
        'X-Legendary-Level',
        'X-Code-Bro-Energy',
        'X-Swiss-Precision'
      ],
    }));

    // Compression and parsing
    this.app.use(compression());
    this.app.use(express.json({ limit: this.isFounderMode ? '50mb' : '10mb' }));
    this.app.use(express.urlencoded({ extended: true, limit: this.isFounderMode ? '50mb' : '10mb' }));

    // Logging
    this.app.use(morgan(this.isFounderMode ? 'combined' : 'combined', {
      stream: {
        write: (message: string) => {
          logger.info(message.trim(), { service: 'express' });
        }
      }
    }));

    // Custom request logger
    this.app.use(requestLogger);

    // Rate limiting (relaxed for founder)
    const rateLimiter = rateLimit({
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: this.isFounderMode ? 10000 : 1000, // Limit each IP to 1000 requests per windowMs (10k for founder)
      message: {
        error: 'Too many requests from this IP, please try again later.',
        retryAfter: '15 minutes',
        founderNote: this.isFounderMode ? '👑 Founder rate limit should never be hit!' : undefined,
      },
      standardHeaders: true,
      legacyHeaders: false,
      skip: (req) => {
        // Skip rate limiting for founder requests
        return this.isFounderMode && req.headers['x-founder-request'] === 'true';
      },
    });
    
    this.app.use('/api/', rateLimiter);

    // Swiss precision validator
    this.app.use(swissPrecisionValidator);

    console.log('✅ Legendary middleware initialized with Swiss precision!');
  }

  // =====================================
  // 🛣️ ROUTES INITIALIZATION 🛣️
  // =====================================

  private initializeRoutes(): void {
    console.log('🛣️ Initializing legendary routes...');

    // Health check
    this.app.get('/health', (req: Request, res: Response) => {
      const healthData = {
        status: 'legendary',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        environment: process.env.NODE_ENV || 'development',
        version: '2.0.0',
        founderMode: this.isFounderMode,
        swissPrecision: true,
        codeBroEnergy: 10,
        message: 'N3EXTPATH Legendary Backend is running with infinite code bro energy! 🎸',
        builtBy: 'RICKROLL187',
        builtAt: '2025-08-06 16:18:30 UTC',
        legendary: '⚙️🎸⚙️ WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! ⚙️🎸⚙️',
      };

      if (this.isFounderMode) {
        Object.assign(healthData, {
          founderMessage: '👑 RICKROLL187 FOUNDER SERVER RUNNING WITH INFINITE POWER! 👑',
          founderEnergy: 'INFINITE',
          legendaryLevel: 10,
        });
      }

      res.status(200).json(healthData);
    });

    // API routes
    this.app.use('/api/auth', authRoutes);
    this.app.use('/api/users', userRoutes);
    this.app.use('/api/performance', performanceRoutes);
    this.app.use('/api/okrs', okrRoutes);
    this.app.use('/api/teams', teamsRoutes);
    this.app.use('/api/notifications', notificationsRoutes);
    this.app.use('/api/analytics', analyticsRoutes);

    // Founder-only routes
    if (this.isFounderMode) {
      this.app.use('/api/founder', founderAuth, founderRoutes);
      console.log('👑 Founder routes initialized with infinite privileges!');
    }

    // API info endpoint
    this.app.get('/api', (req: Request, res: Response) => {
      res.json({
        name: 'N3EXTPATH Legendary Backend API',
        version: '2.0.0',
        description: '🎸 Swiss precision API with infinite code bro energy!',
        endpoints: {
          health: '/health',
          auth: '/api/auth',
          users: '/api/users',
          performance: '/api/performance',
          okrs: '/api/okrs',
          teams: '/api/teams',
          notifications: '/api/notifications',
          analytics: '/api/analytics',
          ...(this.isFounderMode && { founder: '/api/founder' }),
        },
        documentation: '/api/docs',
        websocket: '/socket.io',
        builtBy: 'RICKROLL187',
        builtAt: '2025-08-06 16:18:30 UTC',
        founderMode: this.isFounderMode,
        swissPrecision: true,
        legendaryEnergy: '🚀 INFINITE CODE BRO ENERGY! 🚀',
      });
    });

    console.log('✅ Legendary routes initialized with Swiss precision!');
  }

  // =====================================
  // 🚨 ERROR HANDLING 🚨
  // =====================================

  private initializeErrorHandling(): void {
    console.log('🚨 Initializing legendary error handling...');

    // 404 handler
    this.app.use(notFoundHandler);

    // Global error handler
    this.app.use(errorHandler);

    // Unhandled promise rejection handler
    process.on('unhandledRejection', (reason: unknown, promise: Promise<any>) => {
      logger.error('Unhandled Promise Rejection', { 
        reason, 
        promise,
        founderMode: this.isFounderMode 
      });
    });

    // Uncaught exception handler
    process.on('uncaughtException', (error: Error) => {
      logger.error('Uncaught Exception', { 
        error: error.message, 
        stack: error.stack,
        founderMode: this.isFounderMode 
      });
      
      if (!this.isFounderMode) {
        process.exit(1);
      } else {
        logger.warn('👑 Founder mode: Not exiting on uncaught exception');
      }
    });

    console.log('✅ Legendary error handling initialized!');
  }

  // =====================================
  // 🔌 SOCKET.IO INITIALIZATION 🔌
  // =====================================

  private initializeSocket(): void {
    console.log('🔌 Initializing legendary WebSocket...');

    this.server = createServer(this.app);
    
    this.io = new SocketIOServer(this.server, {
      cors: {
        origin: process.env.FRONTEND_URL || 'http://localhost:3000',
        methods: ['GET', 'POST'],
        credentials: true,
      },
      pingTimeout: this.isFounderMode ? 120000 : 60000, // 2 minutes for founder, 1 minute for others
      pingInterval: this.isFounderMode ? 60000 : 25000,  // 1 minute for founder, 25 seconds for others
    });

    // Initialize WebSocket service
    const websocketService = new WebSocketService(this.io);
    websocketService.initialize();

    if (this.isFounderMode) {
      console.log('👑 Founder WebSocket initialized with infinite connection limits!');
    }

    console.log('✅ Legendary WebSocket initialized with Swiss precision!');
  }

  // =====================================
  // 🚀 SERVER STARTUP 🚀
  // =====================================

  public async start(): Promise<void> {
    try {
      console.log('🚀 Starting legendary server...');

      // Connect to database
      await connectDatabase();
      console.log('✅ Database connected with Swiss precision!');

      // Initialize Redis
      await RedisService.initialize();
      console.log('✅ Redis initialized for legendary caching!');

      // Initialize Email Service
      await EmailService.initialize();
      console.log('✅ Email service ready for legendary communications!');

      // Start server
      this.server.listen(this.port, () => {
        console.log('\n🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
        console.log('🎸                                                                           🎸');
        console.log('🎸    🚀⚙️ N3EXTPATH LEGENDARY BACKEND SERVER RUNNING! ⚙️🚀                🎸');
        console.log('🎸                                                                           🎸');
        console.log(`🎸    📍 Server running on: http://localhost:${this.port}                    🎸`);
        console.log(`🎸    📍 API available at: http://localhost:${this.port}/api                 🎸`);
        console.log(`🎸    📍 Health check: http://localhost:${this.port}/health                  🎸`);
        console.log(`🎸    🔌 WebSocket: http://localhost:${this.port}/socket.io                  🎸`);
        console.log('🎸                                                                           🎸');
        console.log('🎸    ⚙️ Built with Swiss Precision by RICKROLL187                         🎸');
        console.log('🎸    📧 Contact: letstalktech010@gmail.com                                  🎸');
        console.log('🎸    🕒 Built at: 2025-08-06 16:18:30 UTC                                  🎸');
        console.log('🎸    🌅 AFTERNOON LEGENDARY SERVER ENERGY AT 16:18:30!                     🎸');
        console.log('🎸                                                                           🎸');
        
        if (this.isFounderMode) {
          console.log('🎸    👑🎸👑 RICKROLL187 FOUNDER SERVER MODE ACTIVE! 👑🎸👑               🎸');
          console.log('🎸    🚀 INFINITE CODE BRO ENERGY AND LEGENDARY PRIVILEGES!               🎸');
          console.log('🎸    ⚡ FOUNDER API ENDPOINTS AVAILABLE!                                  🎸');
        }
        
        console.log('🎸                                                                           🎸');
        console.log('🎸    🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸');
        console.log('🎸                                                                           🎸');
        console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');

        logger.info('🚀 Legendary server started successfully!', {
          port: this.port,
          environment: process.env.NODE_ENV,
          founderMode: this.isFounderMode,
          timestamp: '2025-08-06 16:18:30 UTC',
          builtBy: 'RICKROLL187',
          energy: 'INFINITE CODE BRO ENERGY! 🎸',
        });
      });

    } catch (error) {
      console.error('🚨 Failed to start legendary server:', error);
      logger.error('Server startup failed', { error, founderMode: this.isFounderMode });
      process.exit(1);
    }
  }

  // =====================================
  // 🛑 GRACEFUL SHUTDOWN 🛑
  // =====================================

  public async shutdown(): Promise<void> {
    console.log('🛑 Shutting down legendary server gracefully...');
    
    try {
      // Close server
      if (this.server) {
        this.server.close();
      }

      // Close WebSocket connections
      if (this.io) {
        this.io.close();
      }

      // Close Redis connection
      await RedisService.disconnect();

      console.log('✅ Legendary server shutdown completed!');
      logger.info('Server shutdown completed gracefully', { 
        founderMode: this.isFounderMode,
        timestamp: new Date().toISOString(),
      });
      
    } catch (error) {
      console.error('🚨 Error during server shutdown:', error);
      logger.error('Server shutdown error', { error, founderMode: this.isFounderMode });
    }
  }
}

// =====================================
// 🎸 SERVER INITIALIZATION 🎸
// =====================================

const server = new LegendaryServer();

// Graceful shutdown handlers
process.on('SIGTERM', async () => {
  console.log('📨 SIGTERM received, shutting down legendary server...');
  await server.shutdown();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('📨 SIGINT received, shutting down legendary server...');
  await server.shutdown();
  process.exit(0);
});

// Start the legendary server
server.start().catch((error) => {
  console.error('🚨 Failed to start legendary server:', error);
  process.exit(1);
});

export default server;

console.log('🎸🎸🎸 LEGENDARY BACKEND SERVER COMPLETE! 🎸🎸🎸');
console.log('Built with Swiss precision by RICKROLL187!');
console.log('Email: letstalktech010@gmail.com');
console.log('WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!');
console.log(`Backend server completed at: 2025-08-06 16:18:30 UTC`);
console.log('⚙️ Server architecture: SWISS PRECISION');
console.log('👑 RICKROLL187 founder server: LEGENDARY');
console.log('🔌 WebSocket integration: MAXIMUM REAL-TIME');
console.log('🌅 AFTERNOON LEGENDARY SERVER ENERGY: INFINITE AT 16:18:30!');
console.log('🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸');
