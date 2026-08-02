// DermaTwin AI — ambient 3D background.
// A field of points connected by faint lines (dermal cell mesh), plus a
// slowly rotating faceted "gem" at the center whose wireframe color
// cycles through the beauty palette (rose -> gold -> orchid). Reacts
// gently to pointer position. Respects prefers-reduced-motion.

function initBackground(canvasId) {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof THREE === "undefined") return;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 60;

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);

  // -------- particle field --------
  const COUNT = 140;
  const positions = new Float32Array(COUNT * 3);
  const speeds = [];
  for (let i = 0; i < COUNT; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 140;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 90;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 60;
    speeds.push(0.02 + Math.random() * 0.05);
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));

  const palette = [new THREE.Color(0xff8fb1), new THREE.Color(0xf6c177), new THREE.Color(0xb98cff)];

  const pointsMaterial = new THREE.PointsMaterial({ color: palette[0], size: 1.6, transparent: true, opacity: 0.75 });
  const points = new THREE.Points(geometry, pointsMaterial);
  scene.add(points);

  const maxLines = COUNT * 6;
  const linePositions = new Float32Array(maxLines * 2 * 3);
  const lineGeometry = new THREE.BufferGeometry();
  lineGeometry.setAttribute("position", new THREE.BufferAttribute(linePositions, 3));
  const lineMaterial = new THREE.LineBasicMaterial({ color: palette[1], transparent: true, opacity: 0.12 });
  const lines = new THREE.LineSegments(lineGeometry, lineMaterial);
  scene.add(lines);

  // -------- centerpiece gem --------
  const gemGeo = new THREE.IcosahedronGeometry(14, 1);
  const gemMat = new THREE.MeshBasicMaterial({ color: palette[0], wireframe: true, transparent: true, opacity: 0.35 });
  const gem = new THREE.Mesh(gemGeo, gemMat);
  gem.position.set(0, 0, -20);
  scene.add(gem);

  const gemInnerGeo = new THREE.IcosahedronGeometry(8, 0);
  const gemInnerMat = new THREE.MeshBasicMaterial({ color: palette[2], wireframe: true, transparent: true, opacity: 0.22 });
  const gemInner = new THREE.Mesh(gemInnerGeo, gemInnerMat);
  gemInner.position.copy(gem.position);
  scene.add(gemInner);

  let mouseX = 0, mouseY = 0;
  window.addEventListener("mousemove", (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  });

  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  const CONNECT_DIST = 18;

  function cycledColor(t) {
    // smoothly interpolate around the 3-stop palette over time
    const n = palette.length;
    const scaled = (t % 1) * n;
    const i = Math.floor(scaled);
    const frac = scaled - i;
    return palette[i].clone().lerp(palette[(i + 1) % n], frac);
  }

  function animate(t) {
    const pos = geometry.attributes.position.array;

    if (!reduceMotion) {
      for (let i = 0; i < COUNT; i++) {
        pos[i * 3 + 1] += Math.sin(t * 0.0003 + i) * speeds[i] * 0.05;
        pos[i * 3] += Math.cos(t * 0.0002 + i) * speeds[i] * 0.04;
      }
      geometry.attributes.position.needsUpdate = true;

      points.rotation.y = mouseX * 0.15;
      points.rotation.x = mouseY * 0.1;
      lines.rotation.y = mouseX * 0.15;
      lines.rotation.x = mouseY * 0.1;

      gem.rotation.y = t * 0.00012;
      gem.rotation.x = t * 0.00007 + mouseY * 0.1;
      gemInner.rotation.y = -t * 0.00018;
      gemInner.rotation.x = -t * 0.00009;

      const cycleT = (t * 0.00006) % 1;
      const c1 = cycledColor(cycleT);
      const c2 = cycledColor(cycleT + 0.33);
      pointsMaterial.color = c1;
      gemMat.color = c1;
      gemInner.material.color = c2;
    }

    let lineCount = 0;
    const lp = lineGeometry.attributes.position.array;
    for (let i = 0; i < COUNT && lineCount < maxLines; i++) {
      for (let j = i + 1; j < COUNT && lineCount < maxLines; j++) {
        const dx = pos[i * 3] - pos[j * 3];
        const dy = pos[i * 3 + 1] - pos[j * 3 + 1];
        const dz = pos[i * 3 + 2] - pos[j * 3 + 2];
        const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
        if (dist < CONNECT_DIST) {
          lp[lineCount * 6] = pos[i * 3];
          lp[lineCount * 6 + 1] = pos[i * 3 + 1];
          lp[lineCount * 6 + 2] = pos[i * 3 + 2];
          lp[lineCount * 6 + 3] = pos[j * 3];
          lp[lineCount * 6 + 4] = pos[j * 3 + 1];
          lp[lineCount * 6 + 5] = pos[j * 3 + 2];
          lineCount++;
        }
      }
    }
    lineGeometry.setDrawRange(0, lineCount * 2);
    lineGeometry.attributes.position.needsUpdate = true;

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);
}
