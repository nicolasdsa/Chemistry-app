(() => {
  const animationMap = {
    fade_in_next: { next: "anim-fade-in-next" },
    slide_out_in: { next: "anim-slide-out-in", current: "anim-slide-out-in-current" },
    zoom_in: { next: "anim-zoom-in" },
  };

  function applyScreenAnimation(currentElement, nextElement, animationKey) {
    const mapping = animationMap[animationKey];
    if (!mapping || !nextElement) {
      if (currentElement && currentElement !== nextElement) {
        currentElement.remove();
      }
      return;
    }

    const nextClass = mapping.next;
    const currentClass = mapping.current;

    if (nextClass) {
      nextElement.classList.add(nextClass);
    }
    if (currentElement && currentClass) {
      currentElement.classList.add(currentClass);
    }

    const cleanup = () => {
      if (nextClass) nextElement.classList.remove(nextClass);
      if (currentElement && currentClass) currentElement.classList.remove(currentClass);
      if (currentElement && currentElement !== nextElement) {
        currentElement.remove();
      }
      nextElement.removeEventListener("animationend", cleanup);
    };

    nextElement.addEventListener("animationend", cleanup);

    if (!nextClass) {
      cleanup();
    }
  }

  window.labAnimations = {
    applyScreenAnimation,
  };
})();
