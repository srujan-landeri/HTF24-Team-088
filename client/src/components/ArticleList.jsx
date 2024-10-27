import ArticleCard from "./ArticleCard";


// ArticleList component
const ArticleList = ({ articles, onLike, onDislike, onSave, onCopyLink}) => {
  return (
    <div className="space-y-6">
      {articles.map((article, index) => (
        <ArticleCard
          key={index}
          article={article}
          onLike={onLike}
          onDislike={onDislike}
          onSave={onSave}
          onCopyLink={onCopyLink}
        />
      ))}
    </div>
  );
};

export default ArticleList;