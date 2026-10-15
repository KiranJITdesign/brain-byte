// ============================================================================
// EcoWatt Twin — 5-Floor 3D Courtyard Digital Twin (frontend/src/App.jsx)
// TIP: If you edit the live preview in the browser, you can also paste updates here.
// ============================================================================
function CourtyardBuilding3D({
    floors,
    activeFloorFilter,
    // 'all' | 'exploded' | 0 | 1 | 2 | 3 | 4
    selectedRoomId,
    onSelectRoom,
    currentHour,
    cameraViewMode,
    // 'courtyard' | 'isometric' | 'top' | 'room_zoom'
    showLabels
  }) {
    var _a;
    const mountRef = (0, import_react40.useRef)(null);
    const sceneRef = (0, import_react40.useRef)(null);
    const cameraRef = (0, import_react40.useRef)(null);
    const floorGroupsRef = (0, import_react40.useRef)({});
    const roomObjectsRef = (0, import_react40.useRef)({});
    const spinningFansRef = (0, import_react40.useRef)([]);
    const speakerRingsRef = (0, import_react40.useRef)([]);
    const targetRef = (0, import_react40.useRef)(new Vector3(0, 4, 0));
    const sphericalRef = (0, import_react40.useRef)({ radius: 42, phi: 0.92, theta: 0.55 });
    const pointerRef = (0, import_react40.useRef)({ isDown: false, startX: 0, startY: 0, moved: false });
    const [hoveredInfo, setHoveredInfo] = (0, import_react40.useState)(null);
    const SCALE = 0.08;
    const toWorldX = (x2, w = 0) => (x2 + w / 2 - 300) * SCALE;
    const toWorldZ = (y2, h = 0) => (y2 + h / 2 - 190) * SCALE;
    (0, import_react40.useEffect)(() => {
      const container = mountRef.current;
      if (!container)
        return;
      const width = container.clientWidth || 860;
      const height = container.clientHeight || 560;
      const scene = new Scene();
      scene.background = new Color(396052);
      scene.fog = new FogExp2(396052, 85e-4);
      sceneRef.current = scene;
      const camera = new PerspectiveCamera(42, width / height, 0.1, 260);
      cameraRef.current = camera;
      const renderer = new WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = PCFSoftShadowMap;
      container.innerHTML = "";
      container.appendChild(renderer.domElement);
      const ambient = new AmbientLight(14412542, 0.78);
      scene.add(ambient);
      const sunLight = new DirectionalLight(16707722, 1.35);
      sunLight.position.set(28, 46, 26);
      sunLight.castShadow = true;
      sunLight.shadow.mapSize.width = 2048;
      sunLight.shadow.mapSize.height = 2048;
      scene.add(sunLight);
      const courtyardLight = new PointLight(3718648, 0.9, 50);
      courtyardLight.position.set(3.4, 14, 0);
      scene.add(courtyardLight);
      const ground = new Mesh(
        new PlaneGeometry(90, 70),
        new MeshStandardMaterial({ color: 462105, roughness: 0.9 })
      );
      ground.rotation.x = -Math.PI / 2;
      ground.position.y = -0.15;
      ground.receiveShadow = true;
      scene.add(ground);
      const grid = new GridHelper(84, 42, 959977, 1976635);
      grid.position.y = -0.12;
      grid.material.opacity = 0.28;
      grid.material.transparent = true;
      scene.add(grid);
      floorGroupsRef.current = {};
      roomObjectsRef.current = {};
      spinningFansRef.current = [];
      speakerRingsRef.current = [];
      const FLOOR_HEIGHT = 3.2;
      INITIAL_FLOORS.forEach((floorData) => {
        const fGroup = new Group();
        fGroup.position.y = floorData.level * FLOOR_HEIGHT;
        scene.add(fGroup);
        floorGroupsRef.current[floorData.level] = fGroup;
        const slabMat = new MeshStandardMaterial({
          color: 993582,
          // Rich architectural teal matching the 2D floor plans!
          roughness: 0.75,
          metalness: 0.1
        });
        const addSlabPiece = (bx, by, bw, bh) => {
          const geo = new BoxGeometry(bw * SCALE, 0.18, bh * SCALE);
          const mesh = new Mesh(geo, slabMat);
          mesh.position.set(toWorldX(bx, bw), 0.09, toWorldZ(by, bh));
          mesh.receiveShadow = true;
          fGroup.add(mesh);
        };
        addSlabPiece(0, 0, 600, 90);
        addSlabPiece(0, 285, 600, 95);
        addSlabPiece(0, 90, 320, 195);
        addSlabPiece(445, 90, 155, 195);
        if (floorData.level === 0) {
          const courtSlab = new Mesh(
            new BoxGeometry(135 * SCALE, 0.16, 195 * SCALE),
            new MeshStandardMaterial({ color: 1265226, roughness: 0.6 })
          );
          courtSlab.position.set(toWorldX(315, 135), 0.08, toWorldZ(90, 195));
          fGroup.add(courtSlab);
          const stepMat = new MeshStandardMaterial({ color: 6583435, roughness: 0.8 });
          for (let s2 = 0; s2 < 6; s2++) {
            const stepMesh = new Mesh(
              new BoxGeometry(9.6, 0.22, 0.65),
              stepMat
            );
            stepMesh.position.set(toWorldX(320, 125), 0.2 + s2 * 0.18, toWorldZ(92 + s2 * 7, 8));
            fGroup.add(stepMesh);
          }
        }
        const pillarMat = new MeshStandardMaterial({ color: 15857145, roughness: 0.35 });
        const pillarGeo = new CylinderGeometry(0.16, 0.16, FLOOR_HEIGHT - 0.18, 12);
        const courtyardPillars = [
          [320, 88],
          [350, 88],
          [380, 88],
          [410, 88],
          [442, 88],
          [320, 284],
          [350, 284],
          [380, 284],
          [410, 284],
          [442, 284],
          [320, 125],
          [320, 165],
          [320, 205],
          [320, 245],
          [442, 125],
          [442, 165],
          [442, 205],
          [442, 245]
        ];
        courtyardPillars.forEach(([px, py]) => {
          const pMesh = new Mesh(pillarGeo, pillarMat);
          pMesh.position.set(toWorldX(px), FLOOR_HEIGHT / 2, toWorldZ(py));
          fGroup.add(pMesh);
        });
        if (floorData.level > 0) {
          const railMat = new MeshPhysicalMaterial({
            color: 13358561,
            transparent: true,
            opacity: 0.55,
            roughness: 0.2
          });
          const nRail = new Mesh(new BoxGeometry(124 * SCALE, 0.85, 0.08), railMat);
          nRail.position.set(toWorldX(320, 124), 0.55, toWorldZ(88));
          fGroup.add(nRail);
          const sRail = new Mesh(new BoxGeometry(124 * SCALE, 0.85, 0.08), railMat);
          sRail.position.set(toWorldX(320, 124), 0.55, toWorldZ(284));
          fGroup.add(sRail);
          const wRail = new Mesh(new BoxGeometry(0.08, 0.85, 196 * SCALE), railMat);
          wRail.position.set(toWorldX(320), 0.55, toWorldZ(88, 196));
          fGroup.add(wRail);
          const eRail = new Mesh(new BoxGeometry(0.08, 0.85, 196 * SCALE), railMat);
          eRail.position.set(toWorldX(442), 0.55, toWorldZ(88, 196));
          fGroup.add(eRail);
        }
        if (floorData.level === 4) {
          const solarMat = new MeshStandardMaterial({
            color: 1920728,
            emissive: 1981066,
            emissiveIntensity: 0.3,
            metalness: 0.6,
            roughness: 0.25
          });
          for (let i = 0; i < 6; i++) {
            const panel = new Mesh(new BoxGeometry(1.4, 0.06, 0.9), solarMat);
            panel.position.set(toWorldX(332 + i * 18), FLOOR_HEIGHT + 0.35, toWorldZ(55));
            panel.rotation.x = 0.35;
            fGroup.add(panel);
          }
        }
        floorData.rooms.forEach((room) => {
          const rw = room.w * SCALE;
          const rd = room.h * SCALE;
          const rh = 2.55;
          const rx = toWorldX(room.x, room.w);
          const rz = toWorldZ(room.y, room.h);
          const rGroup = new Group();
          rGroup.position.set(rx, 0.18, rz);
          fGroup.add(rGroup);
          const floorTileGeo = new BoxGeometry(rw - 0.12, 0.08, rd - 0.12);
          const floorTileMat = new MeshStandardMaterial({
            color: 889992,
            emissive: 1013358,
            emissiveIntensity: 0.35,
            roughness: 0.4
          });
          const floorTile = new Mesh(floorTileGeo, floorTileMat);
          floorTile.position.y = 0.04;
          floorTile.userData = { roomId: room.id, roomName: room.name, floorLevel: floorData.level };
          rGroup.add(floorTile);
          const wallGeo = new BoxGeometry(rw - 0.08, rh, rd - 0.08);
          const wallMat = new MeshPhysicalMaterial({
            color: 1138265,
            transparent: true,
            opacity: 0.26,
            roughness: 0.2,
            depthWrite: false
          });
          const wallShell = new Mesh(wallGeo, wallMat);
          wallShell.position.y = rh / 2;
          wallShell.userData = { roomId: room.id, roomName: room.name, floorLevel: floorData.level };
          rGroup.add(wallShell);
          const edgeGeo = new EdgesGeometry(wallGeo);
          const edgeMat = new LineBasicMaterial({
            color: 14075804,
            // Exact gold-beige wall trim from the reference images!
            transparent: true,
            opacity: 0.85
          });
          const edgeWire = new LineSegments(edgeGeo, edgeMat);
          edgeWire.position.y = rh / 2;
          rGroup.add(edgeWire);
          const fixturesGroup = new Group();
          rGroup.add(fixturesGroup);
          const fanSpinners = [];
          const lightMeshes = [];
          const projectorConeMeshes = [];
          const cctvConeMeshes = [];
          const speakerRingMeshes = [];
          const acMeshes = [];
          const pcScreenMeshes = [];
          const numFans = rw > 8 ? 3 : rw > 4.5 ? 2 : 1;
          for (let f = 0; f < numFans; f++) {
            const fx = numFans === 1 ? 0 : (f - (numFans - 1) / 2) * (rw / (numFans + 0.4));
            const fanMount = new Group();
            fanMount.position.set(fx, rh - 0.25, 0);
            const rod = new Mesh(
              new CylinderGeometry(0.03, 0.03, 0.3, 8),
              new MeshStandardMaterial({ color: 14870768 })
            );
            rod.position.y = 0.12;
            fanMount.add(rod);
            const rotor = new Group();
            const hub = new Mesh(
              new CylinderGeometry(0.18, 0.18, 0.08, 12),
              new MeshStandardMaterial({ color: 3718648, metalness: 0.5 })
            );
            rotor.add(hub);
            for (let b = 0; b < 3; b++) {
              const blade = new Mesh(
                new BoxGeometry(0.75, 0.02, 0.14),
                new MeshStandardMaterial({ color: 16317180 })
              );
              blade.rotation.y = b * Math.PI * 2 / 3;
              blade.position.set(Math.cos(blade.rotation.y) * 0.42, 0, Math.sin(blade.rotation.y) * 0.42);
              rotor.add(blade);
            }
            fanMount.add(rotor);
            fixturesGroup.add(fanMount);
            fanSpinners.push(rotor);
            spinningFansRef.current.push({ rotor, roomId: room.id });
          }
          const numLights = 2;
          for (let l = 0; l < numLights; l++) {
            const lz = (l === 0 ? -1 : 1) * Math.min(0.85, rd * 0.26);
            const tubeMat = new MeshStandardMaterial({
              color: 16710083,
              emissive: 16707722,
              emissiveIntensity: 0.95
            });
            const tube = new Mesh(
              new BoxGeometry(Math.min(rw * 0.65, 3.6), 0.04, 0.09),
              tubeMat
            );
            tube.position.set(0, rh - 0.06, lz);
            fixturesGroup.add(tube);
            lightMeshes.push(tube);
          }
          const cctvGroup = new Group();
          cctvGroup.position.set(-rw / 2 + 0.25, rh - 0.22, -rd / 2 + 0.25);
          const camBody = new Mesh(
            new SphereGeometry(0.14, 10, 10),
            new MeshStandardMaterial({ color: 16317180 })
          );
          cctvGroup.add(camBody);
          const camLed = new Mesh(
            new SphereGeometry(0.05, 8, 8),
            new MeshBasicMaterial({ color: 15680580 })
          );
          camLed.position.set(0.08, -0.04, 0.08);
          cctvGroup.add(camLed);
          const fovConeGeo = new ConeGeometry(0.65, 1.45, 12, 1, true);
          const fovConeMat = new MeshBasicMaterial({
            color: 440020,
            transparent: true,
            opacity: 0.16,
            side: DoubleSide,
            depthWrite: false
          });
          const fovCone = new Mesh(fovConeGeo, fovConeMat);
          fovCone.rotation.x = Math.PI / 2.6;
          fovCone.rotation.z = -Math.PI / 4;
          fovCone.position.set(0.45, -0.38, 0.45);
          cctvGroup.add(fovCone);
          cctvConeMeshes.push(fovCone);
          fixturesGroup.add(cctvGroup);
          const hasProjector = room.equipment.some((e) => e.kind === "projector");
          if (hasProjector) {
            const projBox = new Mesh(
              new BoxGeometry(0.38, 0.14, 0.32),
              new MeshStandardMaterial({ color: 14870768 })
            );
            projBox.position.set(0, rh - 0.26, 0.15);
            fixturesGroup.add(projBox);
            const screenMat = new MeshStandardMaterial({
              color: 3718648,
              emissive: 165063,
              emissiveIntensity: 0.75
            });
            const screenMesh = new Mesh(
              new BoxGeometry(Math.min(1.6, rw * 0.48), 0.95, 0.05),
              screenMat
            );
            screenMesh.position.set(0, rh * 0.55, -rd / 2 + 0.12);
            fixturesGroup.add(screenMesh);
            const beamGeo = new ConeGeometry(0.7, 1.35, 16, 1, true);
            const beamMat = new MeshBasicMaterial({
              color: 3718648,
              transparent: true,
              opacity: 0.22,
              side: DoubleSide,
              depthWrite: false
            });
            const beamMesh = new Mesh(beamGeo, beamMat);
            beamMesh.rotation.x = Math.PI / 2;
            beamMesh.position.set(0, rh * 0.62, -rd / 4);
            fixturesGroup.add(beamMesh);
            projectorConeMeshes.push(beamMesh, screenMesh);
          }
          const hasSpeakers = room.equipment.some((e) => e.kind === "speaker");
          if (hasSpeakers) {
            [-1, 1].forEach((side) => {
              const spk = new Mesh(
                new BoxGeometry(0.18, 0.32, 0.16),
                new MeshStandardMaterial({ color: 1976635 })
              );
              spk.position.set(side * (rw / 2 - 0.22), rh * 0.72, -rd / 4);
              fixturesGroup.add(spk);
              const waveGeo = new RingGeometry(0.12, 0.2, 16);
              const waveMat = new MeshBasicMaterial({
                color: 11032055,
                side: DoubleSide,
                transparent: true,
                opacity: 0.65
              });
              const wave = new Mesh(waveGeo, waveMat);
              wave.rotation.y = Math.PI / 2;
              wave.position.set(side * (rw / 2 - 0.32), rh * 0.72, -rd / 4);
              fixturesGroup.add(wave);
              speakerRingMeshes.push(wave);
              speakerRingsRef.current.push({ wave, roomId: room.id });
            });
          }
          const hasAc = room.equipment.some((e) => e.kind === "ac");
          if (hasAc) {
            const acMat = new MeshStandardMaterial({
              color: 16317180,
              emissive: 959977,
              emissiveIntensity: 0.35
            });
            const acUnit = new Mesh(
              new BoxGeometry(0.95, 0.26, 0.22),
              acMat
            );
            acUnit.position.set(0, rh - 0.35, rd / 2 - 0.16);
            fixturesGroup.add(acUnit);
            acMeshes.push(acUnit);
          }
          const hasPc = room.equipment.some((e) => e.kind === "computer");
          if (hasPc) {
            const cols = Math.min(4, Math.max(2, Math.floor(rw / 1.4)));
            for (let c2 = 0; c2 < cols; c2++) {
              const dx = (c2 - (cols - 1) / 2) * 1.1;
              const desk = new Mesh(
                new BoxGeometry(0.85, 0.45, 0.5),
                new MeshStandardMaterial({ color: 3359061 })
              );
              desk.position.set(dx, 0.25, 0.2);
              fixturesGroup.add(desk);
              const monitorMat = new MeshStandardMaterial({
                color: 3718648,
                emissive: 165063,
                emissiveIntensity: 0.85
              });
              const monitor = new Mesh(
                new BoxGeometry(0.52, 0.34, 0.05),
                monitorMat
              );
              monitor.position.set(dx, 0.64, 0.15);
              fixturesGroup.add(monitor);
              pcScreenMeshes.push(monitor);
            }
          }
          const dbBox = new Mesh(
            new BoxGeometry(0.1, 0.42, 0.32),
            new MeshStandardMaterial({
              color: 16096779,
              emissive: 14251782,
              emissiveIntensity: 0.5
            })
          );
          dbBox.position.set(rw / 2 - 0.12, rh * 0.48, rd / 2 - 0.35);
          fixturesGroup.add(dbBox);
          roomObjectsRef.current[room.id] = {
            rGroup,
            floorTile,
            wallShell,
            edgeWire,
            fanSpinners,
            lightMeshes,
            projectorConeMeshes,
            cctvConeMeshes,
            speakerRingMeshes,
            acMeshes,
            pcScreenMeshes,
            worldPos: new Vector3(rx, floorData.level * FLOOR_HEIGHT + 1.2, rz)
          };
        });
      });
      const updateCamera = () => {
        const { radius, phi, theta } = sphericalRef.current;
        const t = targetRef.current;
        camera.position.x = t.x + radius * Math.sin(phi) * Math.sin(theta);
        camera.position.y = t.y + radius * Math.cos(phi);
        camera.position.z = t.z + radius * Math.sin(phi) * Math.cos(theta);
        camera.lookAt(t);
      };
      updateCamera();
      const raycaster = new Raycaster();
      const mouse = new Vector2();
      const getClickableMeshes = () => {
        const list = [];
        Object.values(roomObjectsRef.current).forEach((obj) => {
          if (obj.rGroup.parent && obj.rGroup.parent.visible) {
            list.push(obj.floorTile, obj.wallShell);
          }
        });
        return list;
      };
      const onPointerDown = (e) => {
        pointerRef.current = { isDown: true, startX: e.clientX, startY: e.clientY, moved: false };
      };
      const onPointerMove = (e) => {
        const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = (e.clientX - rect.left) / rect.width * 2 - 1;
        mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
        if (pointerRef.current.isDown) {
          const dx = e.clientX - pointerRef.current.startX;
          const dy = e.clientY - pointerRef.current.startY;
          if (Math.abs(dx) > 3 || Math.abs(dy) > 3)
            pointerRef.current.moved = true;
          sphericalRef.current.theta -= dx * 75e-4;
          sphericalRef.current.phi = Math.max(0.2, Math.min(Math.PI / 2.1, sphericalRef.current.phi - dy * 65e-4));
          pointerRef.current.startX = e.clientX;
          pointerRef.current.startY = e.clientY;
          updateCamera();
          return;
        }
        raycaster.setFromCamera(mouse, camera);
        const hits = raycaster.intersectObjects(getClickableMeshes(), false);
        if (hits.length > 0) {
          const data = hits[0].object.userData;
          renderer.domElement.style.cursor = "pointer";
          setHoveredInfo({
            roomId: data.roomId,
            roomName: data.roomName,
            floorLevel: data.floorLevel,
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
          });
        } else {
          renderer.domElement.style.cursor = "grab";
          setHoveredInfo(null);
        }
      };
      const onPointerUp = (e) => {
        if (!pointerRef.current.isDown)
          return;
        const moved = pointerRef.current.moved;
        pointerRef.current.isDown = false;
        if (!moved) {
          const rect = renderer.domElement.getBoundingClientRect();
          mouse.x = (e.clientX - rect.left) / rect.width * 2 - 1;
          mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
          raycaster.setFromCamera(mouse, camera);
          const hits = raycaster.intersectObjects(getClickableMeshes(), false);
          if (hits.length > 0) {
            onSelectRoom(hits[0].object.userData.roomId);
          }
        }
      };
      const onWheel = (e) => {
        e.preventDefault();
        sphericalRef.current.radius = Math.max(10, Math.min(72, sphericalRef.current.radius + e.deltaY * 0.03));
        updateCamera();
      };
      const dom = renderer.domElement;
      dom.addEventListener("pointerdown", onPointerDown);
      window.addEventListener("pointermove", onPointerMove);
      window.addEventListener("pointerup", onPointerUp);
      dom.addEventListener("wheel", onWheel, { passive: false });
      const onResize = () => {
        if (!container)
          return;
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
      };
      window.addEventListener("resize", onResize);
      let frameId;
      const clock = new Clock();
      const animate = () => {
        frameId = requestAnimationFrame(animate);
        const elapsed = clock.getElapsedTime();
        spinningFansRef.current.forEach((item) => {
          if (item.rotor.userData.spinning) {
            item.rotor.rotation.y -= 0.18;
          }
        });
        speakerRingsRef.current.forEach((item) => {
          if (item.wave.userData.active) {
            const s2 = 1 + 0.45 * Math.sin(elapsed * 6);
            item.wave.scale.set(s2, s2, 1);
            item.wave.material.opacity = 0.25 + 0.35 * Math.sin(elapsed * 6);
          } else {
            item.wave.material.opacity = 0;
          }
        });
        renderer.render(scene, camera);
      };
      animate();
      return () => {
        cancelAnimationFrame(frameId);
        dom.removeEventListener("pointerdown", onPointerDown);
        window.removeEventListener("pointermove", onPointerMove);
        window.removeEventListener("pointerup", onPointerUp);
        dom.removeEventListener("wheel", onWheel);
        window.removeEventListener("resize", onResize);
        renderer.dispose();
      };
    }, []);
    (0, import_react40.useEffect)(() => {
      const BASE_H = 3.2;
      const EXPLODED_H = 6.2;
      floors.forEach((f) => {
        const fGroup = floorGroupsRef.current[f.level];
        if (!fGroup)
          return;
        if (activeFloorFilter === "all") {
          fGroup.visible = true;
          fGroup.position.y = f.level * BASE_H;
        } else if (activeFloorFilter === "exploded") {
          fGroup.visible = true;
          fGroup.position.y = f.level * EXPLODED_H;
        } else {
          fGroup.visible = f.level === Number(activeFloorFilter);
          fGroup.position.y = 0;
        }
        f.rooms.forEach((room) => {
          const obj = roomObjectsRef.current[room.id];
          if (!obj)
            return;
          const stats = calcRoomStats(room);
          const hourState = getRoomHourState(room, currentHour);
          const isSelected = room.id === selectedRoomId;
          let tileHex = 889992;
          let wallHex = 1138265;
          if (stats.status === "critical") {
            tileHex = 14427686;
            wallHex = 10033947;
          } else if (stats.status === "warning" || hourState.isWastingNow) {
            tileHex = 14251782;
            wallHex = 9584654;
          }
          obj.floorTile.material.color.setHex(tileHex);
          obj.floorTile.material.emissive.setHex(tileHex);
          obj.floorTile.material.emissiveIntensity = isSelected ? 0.85 : 0.35;
          obj.wallShell.material.color.setHex(wallHex);
          obj.wallShell.material.opacity = isSelected ? 0.42 : 0.22;
          obj.edgeWire.material.color.setHex(isSelected ? 2282478 : 14075804);
          const isEqActive = (kind) => room.equipment.some(
            (e) => e.kind === kind && e.is_on && currentHour >= e.start_hour && currentHour < e.end_hour
          );
          const fansOn = isEqActive("fan");
          const lightsOn = isEqActive("light");
          const projOn = isEqActive("projector");
          const spkOn = isEqActive("speaker");
          const acOn = isEqActive("ac");
          const pcOn = isEqActive("computer");
          obj.fanSpinners.forEach((r2) => {
            r2.userData.spinning = fansOn;
          });
          obj.lightMeshes.forEach((m) => {
            m.material.color.setHex(lightsOn ? 16710083 : 3359061);
            m.material.emissiveIntensity = lightsOn ? 1 : 0;
          });
          obj.projectorConeMeshes.forEach((m) => {
            m.visible = projOn;
          });
          obj.speakerRingMeshes.forEach((w) => {
            w.userData.active = spkOn;
          });
          obj.acMeshes.forEach((m) => {
            m.material.emissiveIntensity = acOn ? 0.65 : 0;
          });
          obj.pcScreenMeshes.forEach((m) => {
            m.material.color.setHex(pcOn ? 3718648 : 1976635);
            m.material.emissiveIntensity = pcOn ? 0.9 : 0;
          });
        });
      });
    }, [floors, activeFloorFilter, selectedRoomId, currentHour]);
    (0, import_react40.useEffect)(() => {
      if (!cameraRef.current)
        return;
      if (cameraViewMode === "courtyard") {
        targetRef.current.set(5.5, 6.5, -2.5);
        sphericalRef.current = { radius: 22, phi: 1.18, theta: 0.02 };
      } else if (cameraViewMode === "isometric") {
        targetRef.current.set(0, 4, 0);
        sphericalRef.current = { radius: 44, phi: 0.88, theta: 0.58 };
      } else if (cameraViewMode === "top") {
        targetRef.current.set(0, 0, 0);
        sphericalRef.current = { radius: 42, phi: 0.18, theta: 0 };
      } else if (cameraViewMode === "room_zoom" && selectedRoomId) {
        const obj = roomObjectsRef.current[selectedRoomId];
        if (obj) {
          const yPos = obj.rGroup.parent ? obj.rGroup.parent.position.y + 1.2 : 1.2;
          targetRef.current.set(obj.rGroup.position.x, yPos, obj.rGroup.position.z);
          sphericalRef.current = { radius: 12.5, phi: 0.72, theta: 0.45 };
        }
      }
      const { radius, phi, theta } = sphericalRef.current;
      const t = targetRef.current;
      cameraRef.current.position.set(
        t.x + radius * Math.sin(phi) * Math.sin(theta),
        t.y + radius * Math.cos(phi),
        t.z + radius * Math.sin(phi) * Math.cos(theta)
      );
      cameraRef.current.lookAt(t);
    }, [cameraViewMode, selectedRoomId, activeFloorFilter]);
    return /* @__PURE__ */ import_react40.default.createElement("div", { className: "relative w-full h-full min-h-[520px] rounded-2xl overflow-hidden border border-slate-800 bg-[#050914]" }, /* @__PURE__ */ import_react40.default.createElement("div", { ref: mountRef, className: "w-full h-full min-h-[520px]" }), /* @__PURE__ */ import_react40.default.createElement("div", { className: "pointer-events-none absolute top-3 left-3 right-3 flex flex-wrap items-center justify-between gap-2" }, /* @__PURE__ */ import_react40.default.createElement("div", { className: "px-3.5 py-1.5 rounded-xl bg-slate-950/90 border border-cyan-500/40 backdrop-blur-md shadow-lg" }, /* @__PURE__ */ import_react40.default.createElement("div", { className: "text-[10px] font-bold uppercase tracking-widest text-cyan-400" }, activeFloorFilter === "all" ? "ALL 5 FLOORS \u2022 CENTRAL COURTYARD & ATRIUM VIEW" : activeFloorFilter === "exploded" ? "EXPLODED 5-FLOOR ARCHITECTURAL STACK" : (_a = FLOOR_META[Number(activeFloorFilter)]) == null ? void 0 : _a.banner), /* @__PURE__ */ import_react40.default.createElement("div", { className: "text-xs text-slate-300 font-medium" }, "3D Interior Fixtures Active: Spinning Ceiling Fans \u2022 LED Tubes \u2022 Projectors \u2022 CCTV \u2022 PA Speakers \u2022 Split ACs \u2022 Smart DB")), /* @__PURE__ */ import_react40.default.createElement("div", { className: "px-3 py-1.5 rounded-xl bg-slate-950/90 border border-slate-800 text-xs text-amber-300 font-semibold backdrop-blur-md" }, "Drag to Orbit \u2022 Scroll to Zoom Into Rooms \u2022 Click Any Room")), hoveredInfo && /* @__PURE__ */ import_react40.default.createElement(
      "div",
      {
        className: "pointer-events-none absolute z-20 px-3 py-2 rounded-xl bg-slate-900/95 border border-cyan-400/50 text-xs shadow-xl backdrop-blur-md",
        style: {
          left: Math.min(hoveredInfo.x + 14, 520),
          top: Math.max(hoveredInfo.y - 44, 14)
        }
      },
      /* @__PURE__ */ import_react40.default.createElement("div", { className: "font-bold text-white" }, hoveredInfo.roomName),
      /* @__PURE__ */ import_react40.default.createElement("div", { className: "text-cyan-300 text-[11px]" }, "Floor ", hoveredInfo.floorLevel, " \u2022 Click to inspect Fans, Lights, CCTV & Projector")
    ), /* @__PURE__ */ import_react40.default.createElement("div", { className: "pointer-events-none absolute bottom-3 left-3 flex flex-wrap items-center gap-3 px-3.5 py-2 rounded-xl bg-slate-950/90 border border-slate-800 text-[11px] backdrop-blur-md" }, /* @__PURE__ */ import_react40.default.createElement("span", { className: "flex items-center gap-1.5 text-emerald-400" }, /* @__PURE__ */ import_react40.default.createElement("span", { className: "w-2.5 h-2.5 rounded-full bg-emerald-400" }), " Optimal Room"), /* @__PURE__ */ import_react40.default.createElement("span", { className: "flex items-center gap-1.5 text-amber-400" }, /* @__PURE__ */ import_react40.default.createElement("span", { className: "w-2.5 h-2.5 rounded-full bg-amber-400" }), " After-Hours Warning"), /* @__PURE__ */ import_react40.default.createElement("span", { className: "flex items-center gap-1.5 text-red-400" }, /* @__PURE__ */ import_react40.default.createElement("span", { className: "w-2.5 h-2.5 rounded-full bg-red-500 animate-ping" }), " Critical Wastage"), /* @__PURE__ */ import_react40.default.createElement("span", { className: "text-slate-600" }, "|"), /* @__PURE__ */ import_react40.default.createElement("span", { className: "text-cyan-300" }, "Cyan Cone = CCTV FOV / Projector Beam")));
  }

function Blueprint2DFloorMap({ floorData, selectedRoomId, onSelectRoom, currentHour }) {
    var _a;
    return /* @__PURE__ */ import_react40.default.createElement("div", { className: "relative w-full h-full min-h-[520px] rounded-2xl border border-slate-800 bg-[#051a1d] p-4 flex flex-col items-center justify-center overflow-hidden" }, /* @__PURE__ */ import_react40.default.createElement("div", { className: "mb-2 text-center" }, /* @__PURE__ */ import_react40.default.createElement("div", { className: "text-xs font-bold uppercase tracking-widest text-amber-300" }, (_a = FLOOR_META[floorData.level]) == null ? void 0 : _a.banner), /* @__PURE__ */ import_react40.default.createElement("div", { className: "text-[11px] text-slate-400" }, "Exact 2D Reference Floor Plan \u2022 Click any room to inspect its Fans, Lights, CCTV, Projector & Speakers")), /* @__PURE__ */ import_react40.default.createElement("svg", { viewBox: "0 0 600 380", className: "w-full max-w-[780px] h-auto select-none rounded-xl shadow-2xl border-2 border-[#d6c79c]/60 bg-[#041f24]" }, /* @__PURE__ */ import_react40.default.createElement("text", { x: "382", y: "80", textAnchor: "middle", fill: "#f8fafc", fontSize: "8.5", fontWeight: "700", letterSpacing: "1" }, "PASSAGE / CORRIDOR"), /* @__PURE__ */ import_react40.default.createElement("text", { x: "235", y: "120", textAnchor: "middle", fill: "#f8fafc", fontSize: "8.5", fontWeight: "700", letterSpacing: "1" }, "PASSAGE / CORRIDOR"), /* @__PURE__ */ import_react40.default.createElement("text", { x: "382", y: "296", textAnchor: "middle", fill: "#f8fafc", fontSize: "8.5", fontWeight: "700", letterSpacing: "1" }, "PASSAGE / CORRIDOR"), floorData.level > 0 && /* @__PURE__ */ import_react40.default.createElement("g", null, /* @__PURE__ */ import_react40.default.createElement(
      "rect",
      {
        x: "325",
        y: "88",
        width: "115",
        height: "192",
        rx: "4",
        fill: "#073b42",
        stroke: "#d6c79c",
        strokeWidth: "3"
      }
    ), /* @__PURE__ */ import_react40.default.createElement(
      "rect",
      {
        x: "333",
        y: "96",
        width: "99",
        height: "176",
        fill: "none",
        stroke: "#ffffff",
        strokeWidth: "2.5"
      }
    ), /* @__PURE__ */ import_react40.default.createElement("line", { x1: "333", y1: "96", x2: "432", y2: "272", stroke: "#ffffff", strokeWidth: "2.5" }), /* @__PURE__ */ import_react40.default.createElement("line", { x1: "432", y1: "96", x2: "333", y2: "272", stroke: "#ffffff", strokeWidth: "2.5" })), /* @__PURE__ */ import_react40.default.createElement("g", null, /* @__PURE__ */ import_react40.default.createElement(
      "rect",
      {
        x: "78",
        y: "186",
        width: "42",
        height: "94",
        rx: "3",
        fill: "#073b42",
        stroke: "#d6c79c",
        strokeWidth: "2.5"
      }
    ), /* @__PURE__ */ import_react40.default.createElement("line", { x1: "80", y1: "188", x2: "118", y2: "278", stroke: "#ffffff", strokeWidth: "2" }), /* @__PURE__ */ import_react40.default.createElement("line", { x1: "118", y1: "188", x2: "80", y2: "278", stroke: "#ffffff", strokeWidth: "2" })), floorData.rooms.map((r2) => {
      const stats = calcRoomStats(r2);
      const hourState = getRoomHourState(r2, currentHour);
      const isSelected = r2.id === selectedRoomId;
      let fill = "#0b464c";
      let stroke = "#d6c79c";
      if (stats.status === "critical") {
        fill = "#69191e";
        stroke = "#f87171";
      } else if (stats.status === "warning") {
        fill = "#5c3b11";
        stroke = "#fbbf24";
      }
      return /* @__PURE__ */ import_react40.default.createElement(
        "g",
        {
          key: r2.id,
          onClick: () => onSelectRoom(r2.id),
          className: "cursor-pointer transition-opacity hover:opacity-90"
        },
        /* @__PURE__ */ import_react40.default.createElement(
          "rect",
          {
            x: r2.x,
            y: r2.y,
            width: r2.w,
            height: r2.h,
            rx: "4",
            fill,
            stroke: isSelected ? "#22d3ee" : stroke,
            strokeWidth: isSelected ? "3.5" : "2.2"
          }
        ),
        /* @__PURE__ */ import_react40.default.createElement(
          "path",
          {
            d: `M ${r2.x + 12} ${r2.y + r2.h} A 12 12 0 0 1 ${r2.x} ${r2.y + r2.h - 12}`,
            fill: "none",
            stroke: "#cbd5e1",
            strokeWidth: "1",
            opacity: "0.65"
          }
        ),
        /* @__PURE__ */ import_react40.default.createElement(
          "text",
          {
            x: r2.x + r2.w / 2,
            y: r2.y + r2.h / 2 - 4,
            textAnchor: "middle",
            fill: "#ffffff",
            fontSize: r2.w < 70 ? "6.5" : "8",
            fontWeight: "700"
          },
          r2.code
        ),
        /* @__PURE__ */ import_react40.default.createElement(
          "text",
          {
            x: r2.x + r2.w / 2,
            y: r2.y + r2.h / 2 + 7,
            textAnchor: "middle",
            fill: "#e2e8f0",
            fontSize: "6.2"
          },
          r2.name.length > 24 ? r2.name.slice(0, 22) + "\u2026" : r2.name
        ),
        /* @__PURE__ */ import_react40.default.createElement(
          "text",
          {
            x: r2.x + r2.w / 2,
            y: r2.y + r2.h / 2 + 17,
            textAnchor: "middle",
            fill: stats.wasted_kwh > 0 ? "#fca5a5" : "#6ee7b7",
            fontSize: "6",
            fontWeight: "700"
          },
          stats.daily_kwh,
          " kWh (",
          stats.wasted_kwh > 0 ? `${stats.wasted_kwh} waste` : "OK",
          ")"
        ),
        hourState.isWastingNow && /* @__PURE__ */ import_react40.default.createElement("circle", { cx: r2.x + r2.w - 8, cy: r2.y + 8, r: "4", fill: "#ef4444" })
      );
    })));
  }
