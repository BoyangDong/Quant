select pf.portfolioName, i.instrumentName, p.position, p.positionId  
                from position as p, instrumentName as i, portfolioName as pf 
                where i.instrumentId = p.instrumentId and p.portfolioId = pf.portfolioId and 1=2;