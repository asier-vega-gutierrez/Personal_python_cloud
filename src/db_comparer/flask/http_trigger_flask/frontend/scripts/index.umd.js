

var __accessCheck = (obj, member, msg) => {
  if (!member.has(obj))
    throw TypeError("Cannot " + msg);
};
var __privateGet = (obj, member, getter) => {
  __accessCheck(obj, member, "read from private field");
  return getter ? getter.call(obj) : member.get(obj);
};
var __privateAdd = (obj, member, value) => {
  if (member.has(obj))
    throw TypeError("Cannot add the same private member more than once");
  member instanceof WeakSet ? member.add(obj) : member.set(obj, value);
};
var __privateSet = (obj, member, value, setter) => {
  __accessCheck(obj, member, "write to private field");
  setter ? setter.call(obj, value) : member.set(obj, value);
  return value;
};
(function(factory) {
  typeof define === "function" && define.amd ? define(factory) : factory();
})(function() {

  class Slider {
    constructor() {
      __privateAdd(this, _sliderInstances, void 0);
      __privateSet(this, _sliderInstances, {});
      this.init = () => {
        const sliderElements = document.querySelectorAll('[data-thq="slider"]');
        for (const sliderElement of sliderElements) {
          const identifier = Array.from(sliderElement.classList).join(".");
          const properties = sliderElement.dataset;
          const nextButtons = sliderElement.querySelectorAll(
            '[data-thq="slider-button-next"]'
          );
          const prevButtons = sliderElement.querySelectorAll(
            '[data-thq="slider-button-prev"]'
          );
          const paginationElms = sliderElement.querySelectorAll(
            '[data-thq="slider-pagination"]'
          );
          let nextButton = null;
          let prevButton = null;
          let paginationElm = null;
          for (const next of nextButtons ?? []) {
            if (next.parentNode === sliderElement) {
              nextButton = next;
            }
          }
          for (const prev of prevButtons ?? []) {
            if (prev.parentNode === sliderElement) {
              prevButton = prev;
            }
          }
          for (const pagination22 of paginationElms ?? []) {
            if (pagination22.parentNode === sliderElement) {
              paginationElm = pagination22;
            }
          }
          const autoplay2 = JSON.parse(properties.autoplay ?? "false");
          const autoPlayDelay = JSON.parse(properties.autoplayDelay ?? "3000");
          const loop2 = JSON.parse(properties.loop ?? "false");
          const pagination2 = JSON.parse(properties.pagination ?? "false");
          const disableAutoplayOnInteraction = JSON.parse(
            properties.disableAutoplayOnInteraction ?? "true"
          );
          const pauseAutoplayOnMouseEnter = JSON.parse(
            properties.pauseAutoplayOnMouseEnter ?? "false"
          );
          let autoplayOptions;
          if (!autoplay2) {
            autoplayOptions = null;
          } else if (autoplay2 && !autoPlayDelay && !disableAutoplayOnInteraction && !pauseAutoplayOnMouseEnter) {
            autoplayOptions = true;
          } else {
            autoplayOptions = {
              delay: autoPlayDelay,
              disableOnInteraction: disableAutoplayOnInteraction,
              pauseOnMouseEnter: pauseAutoplayOnMouseEnter
            };
          }
          if (!pagination2 && paginationElm) {
            paginationElm.style.display = "none";
          }
          const modules = [Navigation, Autoplay, Pagination];
          const swiperOptions = {
            modules,
            observeSlideChildren: true,
            navigation: {
              nextEl: nextButton,
              prevEl: prevButton
            },
            ...loop2 && { loop: loop2 },
            ...pagination2 && paginationElm && {
              pagination: {
                el: paginationElm,
                clickable: true,
                renderBullet: (index) => {
                  var _a;
                  const paginationIcon = paginationElm == null ? void 0 : paginationElm.children[index];
                  if (paginationIcon) {
                    return getDOMStringRepresentation(paginationIcon);
                  }
                  if (!paginationIcon && ((_a = paginationElm == null ? void 0 : paginationElm.children) == null ? void 0 : _a[0])) {
                    return getDOMStringRepresentation(paginationElm == null ? void 0 : paginationElm.children[0]);
                  }
                  return getDOMStringRepresentation(paginationElm == null ? void 0 : paginationElm.children[index]);
                }
              }
            },
            ...autoplayOptions && {
              autoplay: autoplayOptions
            }
          };
          const swiperInstance = new Swiper(sliderElement, swiperOptions);
          __privateGet(this, _sliderInstances)[identifier] = swiperInstance;
        }
      };
    }
  }

  _sliderInstances = new WeakMap();
  const getElByDataAttribute = (attribute, value, scope = document) => {
    const el = scope.querySelector(`[data-${attribute}="${value}"]`);
    return el;
  };
  const getAllElByClass = (className) => {
    const elements = document.querySelectorAll(`*[class*="${className}"]`);
    return elements;
  };
  const getAllElementsByDataAttribute = (attribute, value, scope = document) => {
    const elements = scope.querySelectorAll(`[data-${attribute}="${value}"]`);
    return elements;
  };

  class Menu {
    constructor() {
      this.init = () => {
        this.getMenuElementsAndAddEvents();
        this.getMenuElementsAndAddEventsByDataAttrs("type");
        this.getMenuElementsAndAddEventsByDataAttrs("role");
        this.getNavbarElementsAndAddEventsByDataThqAttrs();
        return this;
      };
      this.getMenuElementsAndAddEventsByDataAttrs = (dataAttr) => {
        const allHeaders = getAllElementsByDataAttribute("role", "Header");
        allHeaders.forEach((header) => {
          const burgerBtn = getElByDataAttribute(
            dataAttr,
            "BurgerMenu",
            header
          );
          const mobileMenu = getElByDataAttribute(
            dataAttr,
            "MobileMenu",
            header
          );
          const closeBtn = getElByDataAttribute(
            dataAttr,
            "CloseMobileMenu",
            header
          );
          if (!burgerBtn || !mobileMenu || !closeBtn) {
            return;
          }
          burgerBtn.addEventListener("click", () => {
            mobileMenu.classList.add("teleport-show");
          });
          closeBtn.addEventListener("click", () => {
            mobileMenu.classList.remove("teleport-show");
          });
          mobileMenu.addEventListener("click", (event) => {
            var _a;
            const target = event.target;
            if (target.tagName === "A" && ((_a = target.getAttribute("href")) == null ? void 0 : _a.startsWith("#"))) {
              mobileMenu.classList.remove("teleport-show");
            }
          });
        });
      };
      this.getNavbarElementsAndAddEventsByDataThqAttrs = () => {
        const allNavbars = getAllElementsByDataAttribute(
          "thq",
          "thq-navbar"
        );
        const bodyOverflow = document.body.style.overflow;
        allNavbars.forEach((navbar) => {
          const burgerBtn = getElByDataAttribute(
            "thq",
            "thq-burger-menu",
            navbar
          );
          const mobileMenu = getElByDataAttribute(
            "thq",
            "thq-mobile-menu",
            navbar
          );
          const closeBtn = getElByDataAttribute(
            "thq",
            "thq-close-menu",
            navbar
          );
          if (!burgerBtn || !mobileMenu || !closeBtn) {
            return;
          }
          burgerBtn.addEventListener("click", () => {
            window.addEventListener("click", function checkSameLinkClicked(event) {
              if (!event) {
                return;
              }
              let currentElement = event.target;
              while (currentElement !== document.body && !currentElement.href) {
                currentElement = currentElement.parentNode;
              }
              if (!currentElement.href) {
                return;
              }
              if (!mobileMenu) {
                return;
              }
              if (currentElement.href) {
                document.body.style.overflow = bodyOverflow;
              }
              if (currentElement.pathname === window.location.pathname) {
                mobileMenu.classList.remove("teleport-show");
                mobileMenu.classList.remove("thq-show");
                mobileMenu.classList.remove("thq-translate-to-default");
              }
              this.removeEventListener("click", checkSameLinkClicked);
            });
            document.body.style.overflow = "hidden";
            mobileMenu.classList.add("teleport-show");
            mobileMenu.classList.add("thq-show");
            mobileMenu.classList.add("thq-translate-to-default");
          });
          closeBtn.addEventListener("click", () => {
            document.body.style.overflow = bodyOverflow;
            mobileMenu.classList.remove("teleport-show");
            mobileMenu.classList.remove("thq-show");
            mobileMenu.classList.remove("thq-translate-to-default");
          });
          mobileMenu.addEventListener("click", (event) => {
            const target = event.target;
            if (target instanceof HTMLAnchorElement) {
              mobileMenu.classList.remove("teleport-show");
              mobileMenu.classList.remove("thq-show");
              mobileMenu.classList.remove("thq-translate-to-default");
            }
          });
        });
      };
      this.getMenuElementsAndAddEvents = () => {
        const menuElements = getAllElByClass("teleport-menu-burger");
        if (menuElements.length === 0) {
          return;
        }
        menuElements.forEach((burgerMenuElement) => {
          var _a;
          const mobileMenuElement = ((_a = burgerMenuElement.nextElementSibling) == null ? void 0 : _a.className.includes(
            "teleport-menu-mobile"
          )) ? burgerMenuElement.nextElementSibling : null;
          if (!mobileMenuElement) {
            return;
          }
          const closeMenuElement = mobileMenuElement.querySelector(
            '*[class*="teleport-menu-close"]'
          );
          if (!closeMenuElement) {
            return;
          }
          burgerMenuElement.addEventListener("click", () => {
            mobileMenuElement.classList.add("teleport-show");
          });
          closeMenuElement.addEventListener("click", () => {
            mobileMenuElement.classList.remove("teleport-show");
          });
        });
      };
    }
    get styles() {
      return ``;
    }
  }

  class Accordion {
    constructor() {
      this.init = () => {
        this.getAccordionElementsAndAddEvents("type");
        this.getAccordionElementsAndAddEvents("role");
      };
      this.getAccordionElementsAndAddEvents = (dataAttr) => {
        const allAccordions = getAllElementsByDataAttribute(
          "role",
          "Accordion"
        );
        allAccordions.forEach((accordion) => {
          const accordionHeader = getElByDataAttribute(
            dataAttr,
            "AccordionHeader",
            accordion
          );
          const accordionContent = getElByDataAttribute(
            dataAttr,
            "AccordionContent",
            accordion
          );
          if (!accordionHeader || !accordionContent) {
            return;
          }
          accordionHeader.addEventListener("click", () => {
            accordionContent.style.maxHeight ? accordionContent.style.maxHeight = "" : accordionContent.style.maxHeight = `${accordionContent.scrollHeight}px`;
          });
        });
      };
    }
    get styles() {
      return ``;
    }
  }

  let url = location.href;
  document.body.addEventListener(
    "click",
    () => {
      requestAnimationFrame(() => {
        if (url !== location.href) {
          new Slider().init();
          new Menu().init();
          new Accordion().init();
          url = location.href;
        }
      });
    },
    true
  );
  const initializeComponents = () => {
    new Menu().init();
    new Slider().init();
    new Accordion().init();
  };
  const isReactEnvironment = () => {
    return typeof window.React !== "undefined" && typeof window.ReactDOM !== "undefined";
  };
  const setupMutationObserver = () => {
    const appDiv = document.getElementById("appDiv");
    if (appDiv) {
      const observer = new MutationObserver(() => {
        initializeComponents();
        observer.disconnect();
      });
      observer.observe(document.body, { childList: true });
    } else {
      initializeComponents();
    }
  };
  if (isReactEnvironment()) {
    window.React.useEffect(() => {
      setupMutationObserver();
    }, []);
  } else if (document.readyState === "complete" || document.readyState === "interactive") {
    setupMutationObserver();
  } else {
    document.addEventListener("DOMContentLoaded", () => {
      setupMutationObserver();
    });
  }

});



// Butoms redirections CHOOSE
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('choose_redirect_btn_c1').addEventListener('click', function() {
    window.location.href = '/galery';
  });
});
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('choose_redirect_btn_c2').addEventListener('click', function() {
    window.location.href = '/galery';
  });
});
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('choose_redirect_btn_c3').addEventListener('click', function() {
    window.location.href = '/galery';
  });
});

// Butoms redirections GALERY
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('choose_redirect_btn_g1').addEventListener('click', function() {
    window.open('style/images/001.jpg', '_blank');
  });
});
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('choose_redirect_btn_g2').addEventListener('click', function() {
    window.open('style/images/002.jpg', '_blank');
  });
});
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('choose_redirect_btn_g3').addEventListener('click', function() {
    window.open('style/images/003.jpg', '_blank');
  });
});
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('choose_redirect_btn_g4').addEventListener('click', function() {
    window.open('style/images/004.jpg', '_blank');
  });
});
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('choose_redirect_btn_g5').addEventListener('click', function() {
    window.open('style/images/005.jpg', '_blank');
  });
});
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('choose_redirect_btn_g6').addEventListener('click', function() {
    window.open('style/images/006.jpg', '_blank');
  });
});
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('choose_redirect_btn_g7').addEventListener('click', function() {
    window.open('style/images/007.jpg', '_blank');
  });
});




// Hide the mobile menu
document.addEventListener('DOMContentLoaded', function() {
  // Find the mobile menu "Explore art" button
  const mobileExploreBtn = document.querySelector(
    '[data-role="MobileMenu"] .solidbuttom_button'
  );
  // Find the close button in the mobile menu
  const closeBtn = document.querySelector('[data-role="CloseMobileMenu"]');

  if (mobileExploreBtn && closeBtn) {
    mobileExploreBtn.addEventListener('click', function(e) {
      // Let the anchor scroll to #main-section
      setTimeout(() => {
        closeBtn.click(); // Close the mobile menu after scroll
      }, 1); // Delay to allow scroll
    });
  }
});
