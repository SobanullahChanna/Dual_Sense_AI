import * as THREE from 'three';
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';

// Test: load an FBX file and inspect its animation tracks
async function testFBX(url) {
    const loader = new FBXLoader();
    return new Promise((resolve, reject) => {
        loader.load(url, (obj) => {
            const clip = obj.animations && obj.animations.length > 0 ? obj.animations[0] : null;
            if (!clip) {
                console.log(`❌ ${url}: No animation clip found`);
                resolve(null);
                return;
            }
            const boneNames = new Set();
            clip.tracks.forEach(t => {
                const dot = t.name.lastIndexOf('.');
                if (dot > 0) boneNames.add(t.name.slice(0, dot));
            });
            const hasMixamorig = [...boneNames].some(n => n.toLowerCase().includes('mixamorig'));
            console.log(`📊 ${url}: ${clip.tracks.length} tracks, ${boneNames.size} bones, hasMixamorig=${hasMixamorig}`);
            if (boneNames.size > 0) {
                console.log(`   Bones: [${[...boneNames].slice(0,5).join(', ')}${boneNames.size > 5 ? '...' : ''}]`);
                console.log(`   Duration: ${clip.duration.toFixed(3)}s`);
            }
            resolve({ clip, boneNames, hasMixamorig });
        }, undefined, reject);
    });
}

// Test letters A, D, B, C
async function runTests() {
    console.log('=== FBX Animation Diagnostic ===');
    for (const letter of ['A', 'B', 'C', 'D', 'E', 'G', 'X', 'Z']) {
        try {
            await testFBX(`assets/${letter}.fbx`);
        } catch(e) {
            console.log(`❌ ${letter}.fbx: Load error - ${e.message}`);
        }
    }
    console.log('=== Diagnostic Complete ===');
}

runTests().then(() => console.log('Done'));
