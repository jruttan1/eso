import '../index.css'
import ThemeToggle from './ThemeToggle'
import tree from '../assets/tree.svg'

function Hero({ theme, setTheme }) {
    return (
        <>
        <div className = 'hero'>
            <div className = 'heroContent'>
                <div className = 'title'>
                    eso
                </div>
                <div className = 'subtitle'>
                    a note taking tool that reorganizes your thoughts so you dont have to
                </div>
                <div className = 'landing-text-block'>
                    i wanted to build this as a thesis on intentional design, a learning project, and most importantly a tool i actually needed. as someone with adhd, i noticed everytime i wanted to write something down i’d either lose it in apple notes, or get paralyzed by a notion template. so i built this instead
                </div>
                <div className = 'links'>
                    <a href = 'https://medium.com/@jackjr.ruttan' target="_blank" rel="noreferrer">blog</a> • <a href ='https://github.com/jruttan1/eso' target="_blank" rel="noreferrer">github</a>
                </div>
            </div>
            <div className = 'name'>
                built by jack ruttan
            </div>
            <ThemeToggle theme={theme} setTheme={setTheme}/>
        </div>
        <img className="tree" src={tree} alt=""/>
        </>
    )
}

export default Hero
